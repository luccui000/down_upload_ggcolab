!pip install pyunpack
import requests
import zipfile
import os
import rarfile
from pyunpack import Archive

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def un_zipFiles(path, path2):
    files = os.listdir(path)
    for file in files:
        if file.endswith('.zip'):
            filePath=path+'/'+file
            zip_file = zipfile.ZipFile(filePath)
            for names in zip_file.namelist():
                zip_file.extract(names,path2)
            zip_file.close() 
def un_rarFiles(path, path2):
    files = os.listdir(path)
    for file in files:
        if file.endswith('.rar'):
            filePath=path+'/'+file
            print(filePath)
            rarfile.RarFile(filePath).extractall(path2)
            

def ListFiles(path):
    files = os.listdir(path)
    for file in files:
        if file.endswith('.rar'):
            print(path + '/' + file)               

if __name__ == "__main__":
    file_id = ''
    destination = ''
    save_response_content(file_id, destination)
    print('Saved.')
