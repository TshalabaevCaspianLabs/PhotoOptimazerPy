import os


def get_photo_original():
    os.chdir("ORIGINAL")
    PATH = os.getcwd()

    data = []
    for file in os.listdir():
        data.append(f'{PATH}/{file}')

    return data


def get_photo_download():
    os.chdir("/Users/macbookpro/Documents/PhotoOptimazerPy/PHOTO/DOWNLOAD")
    PATH = os.getcwd()

    data = []
    for file in os.listdir():
        data.append(f'{PATH}/{file}')

    return data