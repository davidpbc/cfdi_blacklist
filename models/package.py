from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, Boolean
from .base import Base, Session

s = Session()


class Package(Base):
    __tablename__ = 'package'
    id = Column(Integer, primary_key=True)
    uuid_pack = Column(String)
    pack_data = Column(LargeBinary)
    downloaded = Column(Boolean)
    # Request
    request_id = Column(ForeignKey('request.id'), nullable=False)
    request = relationship("Request", foreign_keys=request_id)

    def __repr__(self):
        return "<Fiel(name='{}', empresa='{}')>" \
                .format(self.name, self.empresa)

    @classmethod
    def find_by_id(cls, id):
        return s.query(cls).filter_by(id=id).first() or False

    @classmethod
    def find_by_uuid(cls, uuid):
        return s.query(cls).filter_by(uuid_pack=uuid).first() or False

    @classmethod
    def get_by_request_id(cls, request_id):
        return s.query(cls).filter_by(request_id=request_id).all()

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
