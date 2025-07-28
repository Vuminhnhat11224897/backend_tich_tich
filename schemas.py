from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# CustomerSecurity Schemas
class CustomerSecurityBase(BaseModel):
    phone: str
    pin: str

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
    pin: str

class CustomerResponse(CustomerBase):
    user_id: int
    created_at: datetime
    is_active: bool
    security_info: Optional[CustomerSecurityResponse] = None

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
    savings: Optional[int] = 0
    charity: Optional[int] = 0
    spending: Optional[int] = 0
    study: Optional[int] = 0

class WalletCreate(WalletBase):
    child_id: int

class WalletUpdate(WalletBase):
    pass

class WalletResponse(WalletBase):
    wallet_id: int
    child_id: int
    total: int
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
