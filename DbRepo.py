from Db_config import local_session
from User import User
from werkzeug.security import generate_password_hash
import logging
from Logger import Logger
from Customer import Customer


logger = Logger.get_instance()


class DbRepo:

    def __init__(self, local_session):
        self.local_session = local_session
        self.logger = Logger.get_instance()

    def get_customer_by_id(self, id):
        return self.local_session.query(Customer).filter(Customer.id == id).all()

    def get_all_customers(self):
        return self.local_session.query(Customer).all()

    def post(self, object_):
        self.local_session.add(object_)
        self.local_session.commit()

    def update_by_column_value(self, table_class, column_name, value, data):
        self.local_session.query(table_class).filter(column_name == value).update(data)
        self.local_session.commit()

    def get_user_by_id(self, id):
        return self.local_session.query(User).filter(User.id == id).all()

    def get_all_users(self):
        return self.local_session.query(User).all()

    def get_user_by_username(self, username):
        return self.local_session.query(User).filter(User.username == username).all()

    def get_user_by_email(self, email):
        return self.local_session.query(User).filter(User.email == email).all()


    def delete_customer_by_id(self, id):
        self.local_session.query(Customer).filter(Customer.id == id).delete(synchronize_session=False)
        self.local_session.commit()
        logger.logger.info(f' delete customer id {id} ')


    def put_customer_by_id(self, id, data):
        object=self.local_session.query(Customer).filter(Customer.id==id)
        if not object:
            self.local_session.add(object)
        logger.logger.debug(f' someone trying to activate put func and the customer dosent exist, so we add the customer {object} ')
        object.update(data)
        logger.logger.debug(f' updating data  {data} for customer id{id}')
        self.local_session.commit()

    def patch_customer_by_id(self, id, data):
        object=self.local_session.query(Customer).filter(Customer.id==id)
        if not object:
            return
        else:
            object.update(data)
            self.local_session.commit()

    def drop_all_table(self):
        self.local_session.execute(f'DROP TABLE {"customers"} cascade')
        self.local_session.execute(f'DROP TABLE {"users"} cascade')
