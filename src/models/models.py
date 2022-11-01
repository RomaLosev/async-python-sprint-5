from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    username = Column(String(50), unique=True)


class FileModel(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    path = Column(String)
    size = Column(Integer)
    is_downloadable = Column(Boolean)
    author = Column(ForeignKey(User.id))
