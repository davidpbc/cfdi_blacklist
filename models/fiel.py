from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, Boolean, Text, ForeignKey
from .base import Base


class Fiel(Base):
    __tablename__ = 'fiel'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cer_pem = Column(Text, nullable=False)
    key_pem = Column(Text, nullable=False)
    passphrase = Column(String, nullable=False)
    empresa_id = Column(Integer, ForeignKey('empresa.id'))
    empresa = relationship("Empresa", back_populates="fiels")

    def __repr__(self):
        return "<Fiel(name='{}', empresa='{}')>" \
                .format(self.name, self.empresa)
