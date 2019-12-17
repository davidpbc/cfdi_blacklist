# -*- coding: utf-8 -*-
from crud import load_pre_csv, load_def_csv, recreate_table
from models.base import Session
from models.blacklist import Blacklist
import urllib.request
import shutil
import os

s = Session()

# URL General SAT
SAT_URL = "http://omawww.sat.gob.mx/cifras_sat/Documents/"


def recreate_blacklist():
    recreate_table(Blacklist)


def update_blacklist(file_path, definitivos=False):
    if definitivos:
        load_def_csv(file_path)
    else:
        load_pre_csv(file_path)


def download_file(file_path, definitivos=False):
    filename = 'Presuntos.csv'
    if definitivos:
        filename = 'Definitivos.csv'
    try:
        with urllib.request.urlopen(SAT_URL + filename) as res, open(file_path, 'wb') as f:
            shutil.copyfileobj(res, f)
            return True
    except:
        return False


def process_blacklist_update():
    recreate_blacklist()
    script_path = os.path.dirname(__file__)
    path_def = os.path.join(script_path, "Definitivos.csv")
    path_pre = os.path.join(script_path, "Presuntos.csv")
    download_file(path_def, definitivos=True)
    download_file(path_pre)
    update_blacklist(path_def, definitivos=True)
    update_blacklist(path_pre)


if __name__ == '__main__':
    process_blacklist_update()
