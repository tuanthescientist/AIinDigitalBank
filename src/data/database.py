"""
Database utilities and ORM models
"""

from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional

# Base class for all ORM models
Base = declarative_base()


class Customer(Base):
    """Customer ORM Model"""
    __tablename__ = "customers"
    
    customer_id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    kyc_status = Column(String)  # VERIFIED, PENDING, REJECTED
    risk_profile = Column(String)  # CONSERVATIVE, MODERATE, AGGRESSIVE
    total_balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class Product(Base):
    """Product ORM Model"""
    __tablename__ = "products"
    
    product_id = Column(String, primary_key=True)
    name = Column(String)
    product_type = Column(String)  # BONDS, SAVINGS, REALESTATE, INVESTMENT
    min_investment = Column(Float)
    expected_return = Column(Float)
    risk_level = Column(String)  # LOW, MEDIUM, HIGH
    available_quantity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Recommendation(Base):
    """Recommendation ORM Model"""
    __tablename__ = "recommendations"
    
    recommendation_id = Column(String, primary_key=True)
    customer_id = Column(String)
    product_id = Column(String)
    score = Column(Float)
    reason = Column(String)
    accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class DatabaseManager:
    """Database connection and operations manager"""
    
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(bind=self.engine)
    
    def drop_tables(self):
        """Drop all tables"""
        Base.metadata.drop_all(bind=self.engine)
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def close(self):
        """Close engine connection"""
        self.engine.dispose()
