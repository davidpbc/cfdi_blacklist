# -*- coding: utf-8 -*-
import os

# POSTGRESQL Scheme: 'postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>'
# SQLite SCHEME: 'sqlite:///relative_path_to_file.db' or 'sqlite:////absolute/path/to/file.db'

DATABASE_ARGS = {}
DATABASE_URI = 'sqlite:///data.db'

if os.environ.get('DATABASE_URI'):
    DATABASE_URI = os.environ.get('DATABASE_URI')
    DATABASE_ARGS['client_encoding'] = 'utf-8'