from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, TIMESTAMP, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = "customers"
    
    user_id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(15), unique=True, nullable=False, index=True)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    is_active = Column(Boolean, default=True)
    
    # Relationship
    children = relationship("Child", back_populates="parent", cascade="all, delete-orphan")

class Child(Base):
    __tablename__ = "children"
    
    child_id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("customers.user_id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    parent = relationship("Customer", back_populates="children")
    wallet = relationship("Wallet", back_populates="child", uselist=False, cascade="all, delete-orphan")

class Wallet(Base):
    __tablename__ = "wallets"
    
    wallet_id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.child_id", ondelete="CASCADE"), unique=True, nullable=False)
    total = Column(DECIMAL(12, 2), default=0.00)
    savings = Column(DECIMAL(12, 2), default=0.00)
    charity = Column(DECIMAL(12, 2), default=0.00)
    spending = Column(DECIMAL(12, 2), default=0.00)
    bought = Column(DECIMAL(12, 2), default=0.00)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    
    # Relationship
    child = relationship("Child", back_populates="wallet")
