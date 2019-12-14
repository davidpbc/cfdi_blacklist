from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Date, Boolean
from .base import Base, Session
from .fiel import Fiel
from .request import Request

s = Session()


class Empresa(Base):
    __tablename__ = 'empresa'
    id = Column(Integer, primary_key=True)
    rfc = Column(String, nullable=False)
    name = Column(String, nullable=False)
    fiels = relationship(
            'Fiel',
            order_by=Fiel.id,
            backref=backref('fiel'),
            cascade='all, delete, delete-orphan'
    )
    requests = relationship(
        'Request',
        order_by=Request.id,
        backref=backref('request'),
        cascade='all, delete, delete-orphan'
    )

    def __repr__(self):
        return "<Empresa(rfc='{}', name='{}', fiels='{}')>" \
                .format(self.rfc, self.name, self.fiels)

    @classmethod
    def find_by_id(cls, id):
        e = s.query(cls).filter_by(id=id).first()
        if e:
            return e

    @classmethod
    def find_by_rfc(cls, rfc):
        e = s.query(cls).filter_by(rfc=rfc).first()
        if e:
            return e

    @classmethod
    def find_by_name(cls, name):
        e = s.query(cls).filter_by(name=name).first
        if e:
            return e

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
