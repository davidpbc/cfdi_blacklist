from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI, DATABASE_ARGS

engine = create_engine(DATABASE_URI, **DATABASE_ARGS)
Session = sessionmaker(bind=engine)

Base = declarative_base()
