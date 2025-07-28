from sqlalchemy.orm import Session
from models import Customer, Child, Wallet, Transaction, CustomerSecurity
from schemas import CustomerCreate, ChildCreate, WalletUpdate
from decimal import Decimal

# Customer CRUD operations
def create_customer(db: Session, name: str, phone: str, pin: str):
    db_customer = Customer(name=name)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    db_security = CustomerSecurity(user_id=db_customer.user_id, phone=phone, pin=pin)
    db.add(db_security)
    db.commit()
    db.refresh(db_security)
    return db_customer

def get_customer_by_phone(db: Session, phone: str):
    security = db.query(CustomerSecurity).filter(CustomerSecurity.phone == phone).first()
    if security:
        return db.query(Customer).filter(Customer.user_id == security.user_id).first()
    return None

def get_customer_by_id(db: Session, user_id: int):
    return db.query(Customer).filter(Customer.user_id == user_id).first()

# Pin CRUD operations
def get_pin_by_user_id(db: Session, user_id: int):
    security = db.query(CustomerSecurity).filter(CustomerSecurity.user_id == user_id).first()
    if security:
        return security.pin
    return None

def update_pin_by_user_id(db: Session, user_id: int, new_pin: str):
    security = db.query(CustomerSecurity).filter(CustomerSecurity.user_id == user_id).first()
    if security:
        security.pin = new_pin
        db.commit()
        db.refresh(security)
        return True
    return False

# Child CRUD operations
def create_child(db: Session, child: ChildCreate):
    db_child = Child(parent_id=child.parent_id, name=child.name)
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    return db_child

def get_children_by_parent(db: Session, parent_id: int):
    return db.query(Child).filter(Child.parent_id == parent_id).all()

def get_child_by_id(db: Session, child_id: int):
    return db.query(Child).filter(Child.child_id == child_id).first()

# Wallet CRUD operations
def get_wallet_by_child_id(db: Session, child_id: int):
    return db.query(Wallet).filter(Wallet.child_id == child_id).first()

def update_wallet(db: Session, child_id: int, wallet_update: WalletUpdate):
    db_wallet = db.query(Wallet).filter(Wallet.child_id == child_id).first()
    if db_wallet:
        if wallet_update.savings is not None:
            db_wallet.savings = wallet_update.savings
        if wallet_update.charity is not None:
            db_wallet.charity = wallet_update.charity
        if wallet_update.spending is not None:
            db_wallet.spending = wallet_update.spending
            if wallet_update.study is not None:
                db_wallet.study = wallet_update.study
        db.commit()
        db.refresh(db_wallet)
    return db_wallet

# Thêm tiền vào ví
def add_money_to_wallet(db: Session, child_id: int, amount: int, field: str = "total"):
    """
    Cộng tiền vào một trường bất kỳ của ví (total, savings, charity, spending, study)
    """
    db_wallet = db.query(Wallet).filter(Wallet.child_id == child_id).first()
    if db_wallet and hasattr(db_wallet, field):
        setattr(db_wallet, field, getattr(db_wallet, field) + amount)
        db.commit()
        db.refresh(db_wallet)
        return db_wallet
    return None

# Chi tiêu tiền từ ví

def spend_money(db: Session, child_id: int, amount: int, wallet_type: str = 'spending'):
    """
    Chi tiêu trực tiếp từ ví được chỉ định
    wallet_type: 'savings', 'charity', 'spending', 'study', 'total' - ví nào sẽ bị trừ tiền
    """
    db_wallet = db.query(Wallet).filter(Wallet.child_id == child_id).first()
    if not db_wallet or not hasattr(db_wallet, wallet_type):
        return None

    current_balance = getattr(db_wallet, wallet_type)
    if current_balance >= amount:
        setattr(db_wallet, wallet_type, current_balance - amount)
        db.commit()
        db.refresh(db_wallet)
        return db_wallet
    return None  # Không đủ tiền hoặc wallet_type không hợp lệ

# Transaction CRUD
def create_transaction(db: Session, child_id: int, amount: Decimal, type: str, description: str = ""):
    transaction = Transaction(child_id=child_id, amount=amount, type=type, description=description)
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction

def get_transactions_by_child(db: Session, child_id: int):
    return db.query(Transaction).filter(Transaction.child_id == child_id).all()

