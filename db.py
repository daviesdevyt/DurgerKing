from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import dotenv, os
dotenv.load_dotenv()

base = declarative_base()

class User(base):
    __tablename__ = "user"
    id = Column(BigInteger, primary_key=True)
    message = Column(Text, nullable=True)
    package = Column(String(8))
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime)
    username = Column(String(200), default="...")

engine = create_engine(os.getenv("DB_URL"))
connection = engine.connect()
base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()