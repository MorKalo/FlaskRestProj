from Db_config import Base
from sqlalchemy import Column, String,INTEGER

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(INTEGER(), primary_key=True, autoincrement=True)
    fullname = Column(String(50))
    address = Column(String(100))

    def as_dict(self):
        obj_dict = {}
        for c in self.__table__.columns:
            obj_dict[c.name] = getattr(self, c.name)
        return obj_dict

    def __repr__(self):
        return f'\n<id="{self.id}", full_name="{self.fullname}", address="{self.address}">'

    def __str__(self):
        return f'\n<id="{self.id}", full_name="{self.fullname}", address="{self.address}">'
