from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, Boolean
from .base import Base


class Empresa(Base):
    __tablename__ = 'empresa'
    id = Column(Integer, primary_key=True)
    rfc = Column(String, nullable=False)
    name = Column(String, nullable=False)
    fiels = relationship('Fiel', back_populates="empresa")

    def __repr__(self):
        return "<Partner(rfc='{}', name='{}', fiels='{}')>" \
                .format(self.rfc, self.name, self.fiel_ids)
