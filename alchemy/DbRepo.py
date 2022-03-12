from Db_config import local_session
import logging
from Logger import Logger
class DbRepo:


    def __init__(self, local_session):
            self.local_session = local_session
            self.logger = Logger.get_instance()

    def add(self, one_row):
        self.local_session.add(one_row)
        self.local_session.commit()

    def update(self, table_class, id, data):
        local_session.query(table_class).filter(table_class.id == id)\
            .update(data)
        self.local_session.commit()

    def delete(self, table_class, id):
        local_session.query(table_class).filter(table_class.id==id).delete(synchronize_session=False)
        self.local_session.commit()



