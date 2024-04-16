import csv
import os
import numpy as np
import pandas as pd
import requests
import shutil
from sklearn.model_selection import train_test_split

class Data:
    def __init__(self, start_year, end_year, data_path):
        """constructor

        Args:
            start_year (int): first year of data
            end_year (int): last year of data, could the same than start_year
            data_path (string): fullpath of data folder on the host
        """
        def create_folder_if_necessary(path):
            os.makedirs(path , exist_ok=True)
            return path

        self.year_list = [year for year in range(start_year, end_year+1)]
        self.file_list_template = ["carcteristiques", "lieux", "usagers", "vehicules"]
        self.raw_path = create_folder_if_necessary(os.path.join(data_path, "raw"))
        self.cleaned_path = create_folder_if_necessary(os.path.join(data_path, "cleaned"))
        self.preprocessed_path = create_folder_if_necessary(os.path.join(data_path, "preprocessed"))
        self._download_raw_data()
        self._clean_data()  # => caracteristiques.csv, lieux.cav, usagers.csv, vehicules.csv
        self._process_data()  # => X_train.csv, X_test.csv, y_train.csv, y_test.csv


    def _download_raw_data(self):
        """download raw data from https://www.data.gouv.fr
        """
        def download_file(input_url, output_file):
            response = requests.get(input_url)
            if response.status_code == 200:
                # Process the response content as needed
                content = response.text
                text_file = open(output_file, "wb")
                text_file.write(content.encode("utf-8"))  # to be check...
                text_file.close()
            else:
                print(f"Error accessing the object {input_url}:", response.status_code)

        http_url = "https://www.data.gouv.fr/fr/datasets/r/"

        # download list of ressources from gouv.fr
        output_file = os.path.join(self.raw_path, "ressources.csv")
        download_file("https://www.data.gouv.fr/resources.csv", output_file)

        # download data files for each year
        data_files_list = [f'{item}-{year}.csv' for item in self.file_list_template for year in self.year_list]
        with open (output_file, "r", encoding="utf-8") as my_file:
            contents = my_file.readline()
            while contents:
                for filename in data_files_list:
                    if filename in contents:
                        input_url = http_url + contents.split(";")[9][1:-1]  #9 = ressource id
                        output_data_file = os.path.join(self.raw_path, filename)
                        download_file(input_url, output_data_file)
                        break
                contents = my_file.readline()


    def _clean_data(self):

        for file_template in self.file_list_template:
            for year in self.year_list:
                src = os.path.join(self.raw_path, f"{file_template}-{year}.csv")
                dest = os.path.join(self.cleaned_path, f"{file_template}-{year}.csv")
                if file_template == "usagers":
                    # patch usagers file : remove 2nd column
                    with open(src, "r") as source:
                        rdr= csv.reader(source, delimiter=';')
                        with open(dest, "w") as result:
                            wtr= csv.writer(result, delimiter=";", quoting=csv.QUOTE_ALL)
                            for r in rdr:
                                if r:
                                    del r[1]  # 2nd column
                                    wtr.writerow(r)
                else:
                    shutil.copyfile(src, dest)

            # concatenate files on years
            print(file_template)
            if file_template == "carcteristiques":
                output_filename = os.path.join(self.cleaned_path, "caracteristiques.csv")
            else:
                output_filename = os.path.join(self.cleaned_path, f"{file_template}.csv")
            with open(output_filename, "w") as merged_file:
                for index, year in enumerate(self.year_list):
                    input_filename = os.path.join(self.raw_path, f"{file_template}-{year}.csv")
                    with open(input_filename, "r") as file:
                        if index != 0:
                            file.readline()  # Throw away header on all but first file
                        merged_file.write(file.read())


    def _process_data(self):
        """generate X_train.csv, X_test.csv, y_train.csv, y_test.csv files
        """ 
        input_filepath_users = os.path.join(self.cleaned_path, "usagers.csv")
        input_filepath_caract = os.path.join(self.cleaned_path, "caracteristiques.csv")
        input_filepath_places = os.path.join(self.cleaned_path, "lieux.csv")
        input_filepath_veh = os.path.join(self.cleaned_path, "vehicules.csv")

        #--Importing dataset
        df_users = pd.read_csv(input_filepath_users, sep=";")
        df_caract = pd.read_csv(input_filepath_caract, sep=";", header=0, low_memory=False)
        df_places = pd.read_csv(input_filepath_places, sep = ";", encoding='utf-8')
        df_veh = pd.read_csv(input_filepath_veh, sep=";")

        #--Creating new columns
        nb_victim = pd.crosstab(df_users.Num_Acc, "count").reset_index()
        nb_vehicules = pd.crosstab(df_veh.Num_Acc, "count").reset_index()
        df_users["year_acc"] = df_users["Num_Acc"].astype(str).apply(lambda x : x[:4]).astype(int)
        df_users["victim_age"] = df_users["year_acc"]-df_users["an_nais"]
        for i in df_users["victim_age"] :
            if (i>120)|(i<0):
                df_users["victim_age"].replace(i,np.nan)
        df_caract["hour"] = df_caract["hrmn"].astype(str).apply(lambda x : x[:-3])
        df_caract.drop(['hrmn', 'an'], inplace=True, axis=1)
        df_users.drop(['an_nais'], inplace=True, axis=1)

        #--Replacing names 
        df_users.grav.replace([1,2,3,4], [1,3,4,2], inplace = True)
        df_caract.rename({"agg" : "agg_"},  inplace = True, axis = 1)
        corse_replace = {"2A":"201", "2B":"202"}
        df_caract["dep"] = df_caract["dep"].str.replace("2A", "201")
        df_caract["dep"] = df_caract["dep"].str.replace("2B", "202")
        df_caract["com"] = df_caract["com"].str.replace("2A", "201")
        df_caract["com"] = df_caract["com"].str.replace("2B", "202")

        #--Converting columns types
        df_caract[["dep","com", "hour"]] = df_caract[["dep","com", "hour"]].astype(int)

        dico_to_float = { 'lat': float, 'long':float}
        df_caract["lat"] = df_caract["lat"].str.replace(',', '.')
        df_caract["long"] = df_caract["long"].str.replace(',', '.')
        df_caract = df_caract.astype(dico_to_float)

        #--Grouping modalities 
        dico = {1:0, 2:1, 3:1, 4:1, 5:1, 6:1,7:1, 8:0, 9:0}
        df_caract["atm"] = df_caract["atm"].replace(dico)
        catv_value = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,30,31,32,33,34,35,36,37,38,39,40,41,42,43,50,60,80,99]
        catv_value_new = [0,1,1,2,1,1,6,2,5,5,5,5,5,4,4,4,4,4,3,3,4,4,1,1,1,1,1,6,6,3,3,3,3,1,1,1,1,1,0,0]
        df_veh['catv'].replace(catv_value, catv_value_new, inplace = True)

        #--Merging datasets 
        fusion1= df_users.merge(df_veh, on = ["Num_Acc","num_veh", "id_vehicule"], how="inner")
        fusion1 = fusion1.sort_values(by = "grav", ascending = False)
        fusion1 = fusion1.drop_duplicates(subset = ['Num_Acc'], keep="first")
        fusion2 = fusion1.merge(df_places, on = "Num_Acc", how = "left")
        df = fusion2.merge(df_caract, on = 'Num_Acc', how="left")

        #--Adding new columns
        df = df.merge(nb_victim, on = "Num_Acc", how = "inner")
        df.rename({"count" :"nb_victim"},axis = 1, inplace = True) 
        df = df.merge(nb_vehicules, on = "Num_Acc", how = "inner") 
        df.rename({"count" :"nb_vehicules"},axis = 1, inplace = True)

        #--Modification of the target variable  : 1 : prioritary // 0 : non-prioritary
        df['grav'].replace([2,3,4], [0,1,1], inplace=True)

        #--Replacing values -1 and 0 
        col_to_replace0_na = ["trajet", "catv", "motor"]
        col_to_replace1_na = ["trajet", "secu1", "catv", "obsm", "motor", "circ", "surf", "situ", "vma", "atm", "col"]
        df[col_to_replace1_na] = df[col_to_replace1_na].replace(-1, np.nan)
        df[col_to_replace0_na] = df[col_to_replace0_na].replace(0, np.nan)

        #--Dropping columns 
        list_to_drop = ['senc','larrout','actp', 'manv', 'choc', 'nbv', 'prof', 'plan', 'Num_Acc', 'id_vehicule', 'num_veh', 'pr', 'pr1','voie', 'trajet',"secu2", "secu3",'adr', 'v1', 'lartpc','occutc','v2','vosp','locp','etatp', 'infra', 'obs', 'id_usager' ]
        df.drop(list_to_drop, axis=1, inplace=True)

        #--Dropping lines with NaN values
        col_to_drop_lines = ['catv', 'vma', 'secu1', 'obsm', 'atm']
        df = df.dropna(subset = col_to_drop_lines, axis=0)


        target = df['grav']
        feats = df.drop(['grav'], axis = 1)

        X_train, X_test, y_train, y_test = train_test_split(feats, target, test_size=0.3, random_state = 42)

        #--Filling NaN values
        col_to_fill_na = ["surf", "circ", "col", "motor"]
        X_train[col_to_fill_na] = X_train[col_to_fill_na].fillna(X_train[col_to_fill_na].mode().iloc[0])
        X_test[col_to_fill_na] = X_test[col_to_fill_na].fillna(X_train[col_to_fill_na].mode().iloc[0])

        #--Saving the dataframes to their respective output file paths
        for file, filename in zip([X_train, X_test, y_train, y_test], ['X_train', 'X_test', 'y_train', 'y_test']):
            output_filepath = os.path.join(self.preprocessed_path, f'{filename}.csv')
            file.to_csv(output_filepath, index=False)


if __name__ == "__main__":
    from pathlib import Path
    data = Data(2021, 2021, Path(os.path.realpath(__file__)).parents[2])
    print(f"data preprocessed in: {data.preprocessed_path}")
