from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import models
import schemas
from database import SessionLocal, engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tích Tích App API", version="1.0.0")

# Customer endpoints
@app.post("/customers/", response_model=schemas.CustomerResponse)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    # Check if phone already exists
    db_customer = crud.get_customer_by_phone(db, phone=customer.phone)
    if db_customer:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return crud.create_customer(db=db, customer=customer)

@app.get("/customers/", response_model=List[schemas.CustomerResponse])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud.get_customers(db, skip=skip, limit=limit)
    return customers

@app.get("/customers/{user_id}", response_model=schemas.CustomerWithChildren)
def read_customer(user_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_id(db, user_id=user_id)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# Child endpoints
@app.post("/children/", response_model=schemas.ChildResponse)
def create_child(child: schemas.ChildCreate, db: Session = Depends(get_db)):
    # Check if parent exists
    db_customer = crud.get_customer_by_id(db, user_id=child.parent_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Parent not found")
    return crud.create_child(db=db, child=child)

@app.get("/children/parent/{parent_id}", response_model=List[schemas.ChildWithWallet])
def read_children_by_parent(parent_id: int, db: Session = Depends(get_db)):
    children = crud.get_children_by_parent(db, parent_id=parent_id)
    return children

@app.get("/children/{child_id}", response_model=schemas.ChildWithWallet)
def read_child(child_id: int, db: Session = Depends(get_db)):
    db_child = crud.get_child_by_id(db, child_id=child_id)
    if db_child is None:
        raise HTTPException(status_code=404, detail="Child not found")
    return db_child

# Wallet endpoints
@app.get("/wallets/{child_id}", response_model=schemas.WalletResponse)
def read_wallet(child_id: int, db: Session = Depends(get_db)):
    db_wallet = crud.get_wallet_by_child_id(db, child_id=child_id)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return db_wallet

@app.put("/wallets/{child_id}", response_model=schemas.WalletResponse)
def update_wallet(child_id: int, wallet: schemas.WalletUpdate, db: Session = Depends(get_db)):
    db_wallet = crud.update_wallet(db, child_id=child_id, wallet_update=wallet)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return db_wallet

@app.post("/wallets/{child_id}/add-money")
def add_money(child_id: int, amount: float, wallet_type: str, db: Session = Depends(get_db)):
    """
    Thêm tiền vào ví
    wallet_type: savings, charity, spending
    """
    if wallet_type not in ['savings', 'charity', 'spending']:
        raise HTTPException(status_code=400, detail="Invalid wallet type")
    
    from decimal import Decimal
    db_wallet = crud.add_money_to_wallet(db, child_id=child_id, 
                                        amount=Decimal(str(amount)), 
                                        wallet_type=wallet_type)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return {"message": f"Added {amount} to {wallet_type}", "wallet": db_wallet}

@app.post("/wallets/{child_id}/spend")
def spend_money(child_id: int, amount: float, db: Session = Depends(get_db)):
    """
    Chi tiêu từ ví spending
    """
    from decimal import Decimal
    db_wallet = crud.spend_money(db, child_id=child_id, amount=Decimal(str(amount)))
    if db_wallet is None:
        raise HTTPException(status_code=400, detail="Insufficient funds or wallet not found")
    return {"message": f"Spent {amount}", "wallet": db_wallet}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
