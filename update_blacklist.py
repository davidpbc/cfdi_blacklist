# -*- coding: utf-8 -*-
from crud import load_pre_csv, load_def_csv, recreate_table
from models.base import Session
from models.blacklist import Blacklist
import urllib.request
import shutil
import os



s = Session()

print(Blacklist.__tablename__)
recreate_table(Blacklist)

# URL General SAT
url = "http://omawww.sat.gob.mx/cifras_sat/Documents/"
script_path = os.path.dirname(__file__)

path_def = os.path.join(script_path, "Definitivos.csv")
try:
    with urllib.request.urlopen(url + 'Definitivos.csv') as response, open(path_def, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
except:
    pass
load_def_csv(path_def)

path_pre = os.path.join(script_path, "Presuntos.csv")
try:
    with urllib.request.urlopen(url + 'Presuntos.csv') as response, open(path_pre, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
except:
    pass
load_pre_csv(path_pre)

blacklists = s.query(Blacklist).all()