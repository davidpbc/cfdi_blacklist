from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, Boolean, Unicode, ForeignKey
from .base import Base, Session
from datetime import datetime

s = Session()


class Fiel(Base):
    __tablename__ = 'fiel'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cer_pem = Column(Unicode, nullable=False)
    key_pem = Column(Unicode, nullable=False)
    passphrase = Column(String, nullable=False)
    active = Column(Boolean)
    date_init = Column(Date)
    date_end = Column(Date)
    empresa_id = Column(ForeignKey('empresa.id'), nullable=False)
    empresa = relationship("Empresa", foreign_keys=empresa_id)

    def __repr__(self):
        return "<Fiel(name='{}', empresa='{}')>" \
                .format(self.name, self.empresa.name)

    @classmethod
    def find_all(cls):
        return s.query(cls).all()

    @classmethod
    def find_by_name(cls, name):
        return s.query(cls).filter_by(name=name).first() or False

    @classmethod
    def find_by_id(cls, id):
        return s.query(cls).get(id) or False

    @classmethod
    def get_active_fiel(cls, empresa_id):
        f = s.query(cls).filter_by(
            empresa_id=empresa_id, active=True).first()
        if f:
            return f

    @classmethod
    def get_by_empresa_id(cls, empresa_id):
        return s.query(cls).filter_by(empresa_id=empresa_id).all()

    def check_active_fiel(self):
        now = datetime.now()
        if self.date_init > now and self.date_end < now:
            return True

    def save_to_db(self):
        s.add(self)
        s.commit()

    def delete(self):
        s.delete(self)
        s.commit()

    def update(self, values):
        for key, value in values.items():
            setattr(self, key, value)
        
        s.commit()
        s.flush()
