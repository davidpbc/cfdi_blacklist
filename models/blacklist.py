from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean
from .base import Base


class Blacklist(Base):
    __tablename__ = 'blacklist'
    id = Column(Integer, primary_key=True)
    rfc = Column(String, nullable=False)
    name = Column(String, nullable=False)
    csv_line = Column(Integer, nullable=False)
    defi = Column(Boolean)
    pre_fecha = Column(Date)
    def_fecha = Column(Date)

    def __repr__(self):
        return "<Blacklist(rfc='{}', name='{}', defi='{}', pre_fecha='{}', def_fecha='{}')>" \
                .format(self.rfc, self.name, self.defi, self.pre_fecha, self.def_fecha)

    def json(self):
        return {
            'csv_line': self.csv_line,
            'rfc': self.rfc,
            'name': self.name,
            'defi': self.defi,
            'pre_fecha': self.pre_fecha,
            'def_fecha': self.def_fecha,
        }
