from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
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
    last_changed_message = Column(DateTime, nullable=True)
    bots = relationship("Bot")

class Bot(base):
    __tablename__ = "bot"
    id = Column(Integer, primary_key=True)
    phone = Column(String)
    user_id = Column(String(200), ForeignKey("user.username"))

engine = create_engine(os.getenv("DB_URL"))
connection = engine.connect()
base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()