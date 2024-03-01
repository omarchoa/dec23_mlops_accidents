import os
import requests

def download_file(input_url, output_file):
    response = requests.get(input_url)
    if response.status_code == 200:
        # Process the response content as needed
        content = response.text
        text_file = open(output_file, "wb")
        text_file.write(content.encode('utf-8'))  # to be check...
        text_file.close()
        print(f'{output_file} loaded')
    else:
        print(f'Error accessing the object {input_url}:', response.status_code)


def download_raw_data(data_files_list):
    output_path = './data/raw'
    http_url = 'https://www.data.gouv.fr/fr/datasets/r/'

    # download list of ressources from gouv.fr
    output_file = os.path.join(output_path, 'ressources.csv')
    download_file("https://www.data.gouv.fr/resources.csv", output_file)

    # download data files according to data_files_list
    len_data_files = len(data_files_list)
    files_found = 0
    with open (output_file, 'r', encoding='utf-8') as my_file:
        contents = my_file.readline()
        while contents and len_data_files > files_found:
            for filename in data_files_list:
                if filename in contents:
                    files_found += 1
                    input_url = http_url + contents.split(';')[9][1:-1]  #9 = ressource id
                    output_file = os.path.join(output_path, filename)
                    download_file(input_url, output_file)
                    break
            contents = my_file.readline()

    # patch
    src_file = os.path.join(output_path, 'carcteristiques-2021.csv')
    dest_file = os.path.join(output_path, 'caracteristiques-2021.csv')
    os.rename(src_file, dest_file)


if __name__ == '__main__':
    data_files_list = ['carcteristiques-2021.csv', 'lieux-2021.csv', 'usagers-2021.csv', 'vehicules-2021.csv']
    download_raw_data(data_files_list)