from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, TIMESTAMP, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = "customers"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    is_active = Column(Boolean, default=True)
    
    # Relationship
    children = relationship("Child", back_populates="parent", uselist=True, cascade="all, delete-orphan")
    security_info = relationship("CustomerSecurity", back_populates="customer", uselist=False, cascade="all, delete-orphan")
class CustomerSecurity(Base):
    __tablename__ = "customer_security"
    
    user_id = Column(Integer, ForeignKey("customers.user_id", ondelete="CASCADE"), primary_key=True)
    phone = Column(String(15), unique=True, nullable=False)
    pin = Column(String(6), nullable=False)  # Mã PIN 6 số
    
    # Relationship
    customer = relationship("Customer", back_populates="security_info")

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
    total = Column(Integer, default=0)
    savings = Column(Integer, default=0)
    charity = Column(Integer, default=0)
    spending = Column(Integer, default=0)
    study = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    
    # Relationship
    child = relationship("Child", back_populates="wallet")

# Bảng Transaction để lưu các giao dịch
class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.child_id", ondelete="CASCADE"), nullable=False)
    amount = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)  # loại giao dịch: nạp, rút, chuyển, v.v.
    description = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    # Relationship
    child = relationship("Child", backref="transactions")
