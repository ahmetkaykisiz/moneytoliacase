from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import random
import string

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(500), index=True)
    short_code = Column(String(10), unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    clicks = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    @staticmethod
    def generate_short_code(length: int = 6):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length)) 