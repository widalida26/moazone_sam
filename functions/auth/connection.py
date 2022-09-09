import os
import json
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# db_user = os.environ.get('DATABASE_USERNAME')
# db_password = os.environ.get('DATABASE_PASSWORD')
# db_host = os.environ.get('DATABASE_HOST')
# db_port = os.environ.get('DATABASE_PORT')
# db_name = os.environ.get('DATABASE_NAME')

db_secret_name = os.environ['DB_SECRET_NAME']

def get_credentials():
    boto_session = boto3.session.Session()
    try:
        secrets_client = boto_session.client(service_name='secretsmanager', region_name=boto_session.region_name)
        secret_value = secrets_client.get_secret_value(SecretId=db_secret_name)
        secret = secret_value['SecretString']
        secret_json = json.loads(secret)
        username = secret_json['username']
        password = secret_json['password']
        host = secret_json['host']
        port = secret_json['port']
        database = secret_json['dbname']
        return (database, username, password, host, port)
    except Exception as ex:
        raise

class connect_engine:
    try:
        def __init__(self):
            (db_name, db_user, db_password, db_host, db_port) = get_credentials()
            db_url =  f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8"
            print(db_url)
            self.engine = create_engine(db_url, pool_recycle = 500)

        def sessionmaker(self):
            Session = sessionmaker(bind = self.engine)
            session = Session()
            return session

        def connection(self):
            conn = self.engine.connect()
            return conn

    except Exception as ex:
        raise

