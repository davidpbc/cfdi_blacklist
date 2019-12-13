from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Date, Boolean, Unicode, ForeignKey
from .base import Base, Session
from .package import Package

s = Session()


class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    state = Column(String, nullable=False)
    init_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    issuer = Column(Boolean)
    receiver = Column(Boolean)
    # Datos SAT
    uuid_request = Column(String)
    numero_cfdis = Column(Integer)
    mensaje = Column(String)
    cod_estatus = Column(String)
    estado_solicitud = Column(String)
    codigo_estado_solicitud = Column(String)
    # Empresa
    empresa_id = Column(ForeignKey('empresa.id'), nullable=False)
    empresa = relationship("Empresa", foreign_keys=empresa_id)
    # Fiel
    fiel_id = Column(ForeignKey('fiel.id'), nullable=False)
    fiel = relationship("Fiel", foreign_keys=fiel_id)
    # Package
    fiels = relationship(
            'Package',
            order_by=Package.id,
            backref=backref('package'),
            cascade='all, delete, delete-orphan'
    )

    def __repr__(self):
        return "<Request(name='{}', empresa='{}')>" \
                .format(self.name, self.empresa.name)

    @classmethod
    def find_by_id(cls, id):
        return s.query(cls).filter_by(id=id).first() or False

    @classmethod
    def get_by_empresa_id(cls, empresa_id):
        return s.query(cls).filter_by(empresa_id=empresa_id).all()

    def save_to_db(self):
        s.add(self)
        s.commit()

    def delete(self):
        s.delete(self)
        s.commit()