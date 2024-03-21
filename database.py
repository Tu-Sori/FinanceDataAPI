from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


USERNAME = "admin"
PASSWORD = "tusori1234"
HOST = "tusori-rds.ctfdbk5pqtcv.ap-northeast-2.rds.amazonaws.com"
PORT = 3306
DBNAME = "TusoriDB"
DB_URL = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'

class EngineConn:

    def __init__(self):
        self.engine = create_engine(DB_URL, pool_recycle=500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def connection(self):
        conn = self.engine.connect()
        return conn
