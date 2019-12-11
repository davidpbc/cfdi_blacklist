from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, Boolean, Text, ForeignKey
from .base import Base, Session

s = Session()


class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    init_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    # Datos SAT
    uuid_request = Column(String)
    uuid_pack = Column(String)
    numero_cfdis = Column(Integer)
    mensaje = Column(String)
    cod_estatus = Column(String)
    estado_solicitud = Column(String)
    codigo_estado_solicitud = Column(String)
    pack_data = Column(Text)
    # Empresa
    empresa_id = Column(ForeignKey('empresa.id'), nullable=False)
    empresa = relationship("Empresa", foreign_keys=empresa_id)
    # Fiel
    fiel_id = Column(ForeignKey('fiel.id'), nullable=False)
    fiel = relationship("Fiel", foreign_keys=fiel_id)

    def __repr__(self):
        return "<Fiel(name='{}', empresa='{}')>" \
                .format(self.name, self.empresa)

    @classmethod
    def get_by_empresa_id(cls, empresa_id):
        return s.query(cls).filter_by(empresa_id=empresa_id).all()

    def save_to_db(self):
        s.add(self)
        s.commit()

    def delete(self):
        s.delete(self)
        s.commit()