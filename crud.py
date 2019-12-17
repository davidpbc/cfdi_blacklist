# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import create_engine
from config import DATABASE_URI
from models.base import Session, engine, Base
from models.blacklist import Blacklist
from models.empresa import Empresa
from models.fiel import Fiel
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import csv
import chardet

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def recreate_table(table):
    Base.metadata.drop_all(
        engine, tables=[Base.metadata.tables[table.__tablename__]])
    Base.metadata.create_all(
        engine, tables=[Base.metadata.tables[table.__tablename__]])


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def load_def_csv(filename):
    data = {
        'header_row': 2,
        'rfc_col': 1,
        'name_col': 2,
        'def_col': 3,
        'pre_fecha_col': 5,
        'pre_fecha_fmt': "%d/%m/%Y",
        'def_fecha_col': 12,
        'def_fecha_fmt': "%d/%m/%y",
    }
    load_csv(filename, **data)


def load_pre_csv(filename):
    data = {
        'header_row': 2,
        'rfc_col': 1,
        'name_col': 2,
        'def_col': 3,
        'pre_fecha_col': 5,
        'pre_fecha_fmt': "%d/%m/%Y",
        'def_fecha_col': False,
        'def_fecha_fmt': False,
    }
    load_csv(filename, **data)


def load_csv(filename, **kwargs):
    with session_scope() as s:
        header_row = kwargs.get('header_row') or 2
        rfc_col = kwargs.get('rfc_col') or 1
        name_col = kwargs.get('name_col') or 2
        def_col = kwargs.get('def_col') or 3
        pre_fecha_col = kwargs.get('pre_fecha_col') or 5
        pre_fecha_fmt = kwargs.get('pre_fecha_fmt') or "%d/%m/%Y"
        def_fecha_col = kwargs.get('def_fecha_col') or False
        def_fecha_fmt = kwargs.get('def_fecha_fmt') or False

        with open(filename, 'rb') as f:
            try:
                encoding = chardet.detect(f.read()).get('encoding')
            except Exception:
                encoding = "utf-8"

        with open(filename, encoding=encoding) as f:
            csv_reader = csv.reader(f, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > header_row and (
                    'XXXXX' not in row[rfc_col] and row[rfc_col] not in ''):
                    data = {
                        'rfc': row[rfc_col],
                        'name': row[name_col],
                        'csv_line': line_count + 1,
                    }
                    if row[def_col] in ['Definitivo', 'DEFINITIVO', 'definitivo']:
                        data['defi'] = True
                    else:
                        data['defi'] = False

                    # Fecha Publicación Página del SAT Presuntos
                    if row[pre_fecha_col]:
                        try:
                            data['pre_fecha'] = datetime.strptime(row[pre_fecha_col], pre_fecha_fmt)
                        except Exception:
                            print('Error Fecha Presuntos Fila {}'.format(line_count + 1))
                            raise
                    if def_fecha_col and row[def_fecha_col]:
                        try:
                            data['def_fecha'] = datetime.strptime(row[def_fecha_col], def_fecha_fmt)
                        except Exception:
                            print('Error Fecha Definitivos Fila {}'.format(line_count + 1))
                    print("Adding {}-{}".format(data.get('rfc'), data.get('name')))
                    blacklist = Blacklist(**data)
                    s.add(blacklist)
                line_count += 1


def find_by_rfc(rfcs):
    with session_scope() as s:
        q = s.query(Blacklist)
        q = q.filter(Blacklist.rfc.in_(rfcs)).all()
        if q:
            a = []
            for res in q:
                a.append(res.json())
            return a
        else :
            return False


if __name__ == '__main__':
    recreate_database()
