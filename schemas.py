from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# CustomerSecurity Schemas
class CustomerSecurityBase(BaseModel):
    phone: str

class CustomerSecurityCreate(CustomerSecurityBase):
    pass

class CustomerSecurityResponse(CustomerSecurityBase):
    user_id: int

    class Config:
        from_attributes = True

# Customer Schemas
class CustomerBase(BaseModel):
    name: str

class CustomerCreate(CustomerBase):
    phone: str
    
class CustomerResponse(CustomerBase):
    user_id: int
    created_at: datetime
    security_info: Optional[CustomerSecurityResponse] = None

    class Config:
        from_attributes = True

# Child Schemas
class ChildBase(BaseModel):
    name: str
    parent_id: int
    age : int

class ChildCreate(ChildBase):
    pass

class ChildResponse(ChildBase):
    child_id: int
    coin : int
    created_at: datetime
    is_active: bool


    class Config:
        from_attributes = True

# Wallet Schemas
class WalletBase(BaseModel):
    total : Optional[int] = 0
    savings: Optional[int] = 0
    charity: Optional[int] = 0
    joy: Optional[int] = 0
    study: Optional[int] = 0

class WalletCreate(WalletBase):
    child_id: int

class WalletUpdate(WalletBase):
    pass

class WalletResponse(WalletBase):
    wallet_id: int
    child_id: int
    total: int
    savings: int
    charity: int
    joy: int
    study: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Transaction Schemas
class TransactionBase(BaseModel):
    amount: int
    type: str
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    child_id: int

class TransactionResponse(TransactionBase):
    transaction_id: int
    child_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Combined Response Schemas
class ChildWithWallet(ChildResponse):
    wallet: Optional[WalletResponse] = None

class CustomerWithChildren(CustomerResponse):
    children: List[ChildWithWallet] = []
