import time
from requests import HTTPError
from sqlalchemy import MetaData, QueuePool, create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DisconnectionError, TimeoutError
from custom_logger import log

log.info("Setting db configuration")

def retry(func):
    def wrapper(*args, **kwargs):
        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                return func(*args, **kwargs)
            except (DisconnectionError, TimeoutError, HTTPError) as e:
                log.error(f"Error connecting to database: {e}")
                log.info(f"Retrying database connection count - {retries}")
                retries += 1
                time.sleep(5)
        raise Exception("Failed to connect to database after multiple retries.")
    return wrapper

@retry
def create_db_engine():
    connection_url = "mysql+pymysql://root:@localhost:3306/mysql" # I read that I should be using SQL but at the current moment 
                                                                  # I can't setup the server due to a conflict with another driver. 
                                                                  # I'll be using mysql with XAMPP to test it out.
                                                                  # Also, I didn't have enough time to set it up on cloud.

    return create_engine(
        connection_url,
        poolclass=QueuePool,
        pool_size=30,
        max_overflow=0,
        pool_pre_ping=True,
    )

engine = create_db_engine()

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, expire_on_commit=False, bind=engine
)

metadata_obj = MetaData(schema="dbo")
Base = declarative_base(metadata=metadata_obj)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
