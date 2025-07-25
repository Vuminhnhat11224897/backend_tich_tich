from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Optional
from decimal import Decimal
import crud
import models
import schemas
from database import get_db

router = APIRouter(
    prefix="/wallets",
    tags=["wallets"]
)

@router.get("/{child_id}", response_model=schemas.WalletResponse)
def read_wallet(child_id: int, db: Session = Depends(get_db)):
    db_wallet = crud.get_wallet_by_child_id(db, child_id=child_id)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return db_wallet

@router.put("/{child_id}", response_model=schemas.WalletResponse)
def update_wallet(child_id: int, wallet: schemas.WalletUpdate, db: Session = Depends(get_db)):
    db_wallet = crud.update_wallet(db, child_id=child_id, wallet_update=wallet)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return db_wallet

@router.post("/{child_id}/add-money")
def add_money(child_id: int, total: float = Body(..., embed=True), db: Session = Depends(get_db)):
    total_input = Decimal(str(total))
    db_wallet = crud.add_total_money(db, child_id=child_id, total=total_input)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    transaction = models.Transaction(
        child_id=child_id,
        amount=total_input,
        type="add_total",
        description=f"Nạp vào tài khoản gốc: {total}"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return {
        "message": f"Added {total} to main account",
        "wallet": db_wallet,
        "transaction": {
            "id": transaction.transaction_id,
            "amount": str(transaction.amount),
            "type": transaction.type,
            "description": transaction.description,
            "created_at": transaction.created_at
        }
    }

@router.post("/{child_id}/split-money")
def split_money(
    child_id: int,
    savings: Optional[float] = Body(None, embed=True),
    charity: Optional[float] = Body(None, embed=True),
    spending: Optional[float] = Body(None, embed=True),
    study: Optional[float] = Body(None, embed=True),
    db: Session = Depends(get_db)
):
    transactions = []
    db_wallet = crud.get_wallet_by_child_id(db, child_id=child_id)
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if savings is not None and savings > 0:
        crud.add_savings(db, child_id, Decimal(str(savings)))
        transaction = models.Transaction(
            child_id=child_id,
            amount=Decimal(str(savings)),
            type="add_savings",
            description=f"Nhận tiền vào ví savings: {savings}"
        )
        db.add(transaction)
        transactions.append(transaction)

    if charity is not None and charity > 0:
        crud.add_charity(db, child_id, Decimal(str(charity)))
        transaction = models.Transaction(
            child_id=child_id,
            amount=Decimal(str(charity)),
            type="add_charity",
            description=f"Nhận tiền vào ví charity: {charity}"
        )
        db.add(transaction)
        transactions.append(transaction)

    if spending is not None and spending > 0:
        crud.add_spending(db, child_id, Decimal(str(spending)))
        transaction = models.Transaction(
            child_id=child_id,
            amount=Decimal(str(spending)),
            type="add_spending",
            description=f"Nhận tiền vào ví spending: {spending}"
        )
        db.add(transaction)
        transactions.append(transaction)

    if study is not None and study > 0:
        crud.add_study(db, child_id, Decimal(str(study)))
        transaction = models.Transaction(
            child_id=child_id,
            amount=Decimal(str(study)),
            type="add_study",
            description=f"Nhận tiền vào ví study: {study}"
        )
        db.add(transaction)
        transactions.append(transaction)

    if not transactions:
        raise HTTPException(status_code=400, detail="Không có loại ví nào được truyền số tiền hợp lệ")

    db.commit()
    for transaction in transactions:
        db.refresh(transaction)

    db_wallet = crud.get_wallet_by_child_id(db, child_id=child_id)
    return {
        "message": "Split money to wallets",
        "wallet": db_wallet,
        "transactions": [
            {
                "id": t.transaction_id,
                "amount": str(t.amount),
                "type": t.type,
                "description": t.description,
                "created_at": t.created_at
            } for t in transactions
        ]
    }

@router.post("/{child_id}/spend")
def spend_money(
    child_id: int,
    amount: float = Body(..., embed=True),
    wallet_type: str = Body("spending", embed=True),
    db: Session = Depends(get_db)
):
    db_wallet = crud.spend_money(db, child_id=child_id, amount=Decimal(str(amount)), wallet_type=wallet_type)
    if db_wallet is None:
        raise HTTPException(status_code=400, detail="Insufficient funds or wallet not found")
    transaction = models.Transaction(
        child_id=child_id,
        amount=Decimal(str(amount)),
        type=f"spend_{wallet_type}",
        description=f"Chi tiêu {amount} từ ví {wallet_type}"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return {
        "message": f"Spent {amount} from {wallet_type} wallet",
        "wallet": db_wallet,
        "transaction": {
            "id": transaction.transaction_id,
            "amount": str(transaction.amount),
            "type": transaction.type,
            "description": transaction.description,
            "created_at": transaction.created_at
        }
    }