import sys
from datetime import datetime
from DbRepo import DbRepo
from sqlalchemy import asc, text, desc
from Customer import Customer
from User import User
from datetime import *
from Db_config import local_session, create_all_entities

class Init_db():

    def __init__(self):
        self.repo=DbRepo(local_session)


    def reset_all_db(self):
     #   self.repo.drop_all_table()
        create_all_entities()

    def insert_Data(self):
        # add customers
        self.repo.post(Customer(id=234, fullname='Efi Moshe', address='Rishon Le Zion'))
        self.repo.post(Customer(id=789, fullname='Roi Kalo', address='Yavne'))
        # add users
        self.repo.post(User(public_id='12345678', username='EfiMo', email='efi@gmail.com', password='efi1234'))
        self.repo.post(User(public_id='910111213', username='Roiki', email='roiki@gmail.com', password='roi1234'))


