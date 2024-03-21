from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DBNAME = os.getenv("DBNAME")

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    USERNAME, PASSWORD, HOST, PORT, DBNAME
)

class EngineConn:

    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=500)

    def sessionmaker(self):
        Session = sessionmaker(autocommit=False, bind=self.engine)
        return Session()

    def connection(self):
        conn = self.engine.connect()
        return conn
