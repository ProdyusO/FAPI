from sqlalchemy import create_engine, MetaData
import databases


SQLALCHEMY_DATABASE_URL = "sqlite:///./user_database.db"

database = databases.Database(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

metadata = MetaData()
