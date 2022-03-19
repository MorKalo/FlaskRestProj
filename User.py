from sqlalchemy import Column, Integer,BigInteger, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from Db_config import Base


class User(Base):
    __tablename__ = 'users'

    id=Column(Integer(), primary_key=True, autoincrement=True)
    public_id=Column(String(50),unique=True )
    username=Column(String(50), nullable=False)
    email=Column(String(70), nullable=False, unique=True)
    password=Column(String(100), nullable=False)


    def as_dict(self):
        obj_dict = {}
        for c in self.__table__.columns:
            obj_dict[c.name] = getattr(self, c.name)
        return obj_dict

    def __repr__(self):
        return f'\n<id={self.id} public_id={self.public_id} username={self.username} email={self.email} ' \
               f'password={self.password}>'

    def __str__(self):
        return f'\n<id={self.id} public_id={self.public_id} username={self.username} email={self.email} ' \
               f'password={self.password}>'