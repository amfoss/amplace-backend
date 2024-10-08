from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    SmallInteger,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from config import config, curr_env

engine = create_engine(config["SQL_URI"])
Session = sessionmaker(bind=engine)
Base = declarative_base()
DB_URL = "" if curr_env == "production" else "localhost"

@dataclass
class Pixel(Base):
    __tablename__ = "pixel"
    pid = Column(Integer, primary_key=True, autoincrement=True)
    x: int = Column(SmallInteger, default=None)
    y: int = Column(SmallInteger, default=None)
    user: str = Column(String(200), default=None)
    color_hex: str = Column(String(30), default=" #ffffff")

Base.metadata.create_all(engine) 
