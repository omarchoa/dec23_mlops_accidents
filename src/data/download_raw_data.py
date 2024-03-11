import csv
import os
import requests
import shutil

def download_file(input_url, output_file):
    response = requests.get(input_url)
    if response.status_code == 200:
        # Process the response content as needed
        content = response.text
        text_file = open(output_file, "wb")
        text_file.write(content.encode("utf-8"))  # to be check...
        text_file.close()
        print(f"{output_file} loaded")
    else:
        print(f"Error accessing the object {input_url}:", response.status_code)


def download_raw_data(year_list):
    output_path = "./data/raw"
    http_url = "https://www.data.gouv.fr/fr/datasets/r/"

    # download list of ressources from gouv.fr
    output_file = os.path.join(output_path, "ressources.csv")
    download_file("https://www.data.gouv.fr/resources.csv", output_file)

    # download data files according to the year list
    file_list_template = ["carcteristiques", "lieux", "usagers", "vehicules"]
    data_files_list = [f'{item}-{year}.csv' for item in file_list_template for year in year_list]
    len_data_files = len(data_files_list)

    with open (output_file, "r", encoding="utf-8") as my_file:
        contents = my_file.readline()
        while contents:
            for filename in data_files_list:
                if filename in contents:
                    input_url = http_url + contents.split(";")[9][1:-1]  #9 = ressource id
                    output_data_file = os.path.join(output_path, filename)
                    download_file(input_url, output_data_file)
                    break
            contents = my_file.readline()

    # patches
    for year in year_list:
        # patch caracteristiques filename
        src_file = os.path.join(output_path, f"carcteristiques-{year}.csv")
        dest_file = os.path.join(output_path, f"caracteristiques-{year}.csv")
        os.rename(src_file, dest_file)

        # patch usagers file : remove 2nd column
        src = os.path.join(output_path, f"usagers-{year}.csv")
        dest = os.path.join(output_path, f"_usagers-{year}.csv")
        shutil.copyfile(src, dest)
        with open(dest, "r") as source:
            rdr= csv.reader(source, delimiter=';')
            with open(src, "w") as result:
                wtr= csv.writer(result, delimiter=";", quoting=csv.QUOTE_ALL)
                for r in rdr:
                    if r:
                        del r[1]  # 2nd column
                        wtr.writerow(r)


if __name__ == "__main__":
    download_raw_data([2021, 2022])