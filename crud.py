from sqlalchemy.orm import Session
from models import Customer, Child, Wallet
from schemas import CustomerCreate, ChildCreate, WalletUpdate
from decimal import Decimal

# Customer CRUD operations
def create_customer(db: Session, customer: CustomerCreate):
    db_customer = Customer(
        phone=customer.phone,
        name=customer.name
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer_by_phone(db: Session, phone: str):
    return db.query(Customer).filter(Customer.phone == phone).first()

def get_customer_by_id(db: Session, user_id: int):
    return db.query(Customer).filter(Customer.user_id == user_id).first()

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
def add_total_money(db: Session, child_id: int, total: Decimal):
    db_wallet = db.query(Wallet).filter(Wallet.child_id == child_id).first()
    if db_wallet:
        db_wallet.total = total
        db.commit()
        db.refresh(db_wallet)
    return db_wallet

# Chia vào 4 loại ví, đồng bộ với endpoint mới
def add_savings(db: Session, child_id: int, amount: Decimal):
    db_wallet = db.query(Wallet).filter(Wallet.child_id == child_id).first()
    if db_wallet:
        db_wallet.savings += amount
        db.commit()
        db.refresh(db_wallet)
    return db_wallet

def add_charity(db: Session, child_id: int, amount: Decimal):
    db_wallet = db.query(Wallet).filter(Wallet.child_id == child_id).first()
    if db_wallet:
        db_wallet.charity += amount
        db.commit()
        db.refresh(db_wallet)
    return db_wallet

def add_spending(db: Session, child_id: int, amount: Decimal):
    db_wallet = db.query(Wallet).filter(Wallet.child_id == child_id).first()
    if db_wallet:
        db_wallet.spending += amount
        db.commit()
        db.refresh(db_wallet)
    return db_wallet

def add_study(db: Session, child_id: int, amount: Decimal):
    db_wallet = db.query(Wallet).filter(Wallet.child_id == child_id).first()
    if db_wallet:
        db_wallet.study += amount
        db.commit()
        db.refresh(db_wallet)
    return db_wallet

def spend_money(db: Session, child_id: int, amount: Decimal, wallet_type: str = 'spending'):
    """
    Chi tiêu trực tiếp từ ví được chỉ định
    wallet_type: 'savings', 'charity', 'spending', study - ví nào sẽ bị trừ tiền
    """
    db_wallet = db.query(Wallet).filter(Wallet.child_id == child_id).first()
    if not db_wallet:
        return None
    
    # Kiểm tra số dư và trừ tiền từ ví tương ứng
    if wallet_type == 'savings' and db_wallet.savings >= amount:
        db_wallet.savings -= amount
    elif wallet_type == 'charity' and db_wallet.charity >= amount:
        db_wallet.charity -= amount
    elif wallet_type == 'spending' and db_wallet.spending >= amount:
        db_wallet.spending -= amount
    elif wallet_type == 'study' and db_wallet.study >= amount:
        db_wallet.study -= amount
    else:
        return None  # Không đủ tiền hoặc wallet_type không hợp lệ
    db.commit()
    db.refresh(db_wallet)
    return db_wallet
