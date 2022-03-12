from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from configparser import ConfigParser
from Logger import Logger
from sqlalchemy.exc import OperationalError
import logging

config = ConfigParser()
config.read("config.conf")
connection_string = config["db"]["conn_string"]

logger = Logger.get_instance()
Base = declarative_base()

Session = sessionmaker()
engine = create_engine(connection_string, echo=True)  # echo makes the console print all the sql statements being run
local_session = Session(bind=engine)

# creates a table to all classes that inherits from Base
def create_all_entities():
    try:
        Base.metadata.create_all(engine)
        logger.logger.debug('Created all sql tables.')
    except OperationalError:
        print('The database does not exist, please check the connection string')
        logger.logger.critical('The database does not exist, please check the connection string')