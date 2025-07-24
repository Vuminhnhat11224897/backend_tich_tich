from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional, List

# Customer Schemas
class CustomerBase(BaseModel):
    phone: str

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    user_id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

# Child Schemas
class ChildBase(BaseModel):
    name: str
    parent_id: int

class ChildCreate(ChildBase):
    pass

class ChildResponse(ChildBase):
    child_id: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

# Wallet Schemas
class WalletBase(BaseModel):
    savings: Optional[Decimal] = Decimal('0.00')
    charity: Optional[Decimal] = Decimal('0.00')
    spending: Optional[Decimal] = Decimal('0.00')
    bought: Optional[Decimal] = Decimal('0.00')

class WalletCreate(WalletBase):
    child_id: int

class WalletUpdate(WalletBase):
    pass

class WalletResponse(WalletBase):
    wallet_id: int
    child_id: int
    total: Decimal
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Combined Response Schemas
class ChildWithWallet(ChildResponse):
    wallet: Optional[WalletResponse] = None

class CustomerWithChildren(CustomerResponse):
    children: List[ChildWithWallet] = []
