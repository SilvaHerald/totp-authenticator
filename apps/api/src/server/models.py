from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    
    sync_data = relationship("SyncData", back_populates="owner", uselist=False)

class SyncData(Base):
    __tablename__ = "sync_data"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    last_updated = Column(Float, nullable=False, default=0.0)
    encrypted_payload = Column(String, nullable=True)
    
    owner = relationship("User", back_populates="sync_data")
