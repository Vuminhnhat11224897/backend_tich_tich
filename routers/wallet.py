from attr import In
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
    amount = int(total)
    db_wallet = crud.add_money_to_wallet(db, child_id=child_id, amount=amount, field="total")
    if db_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    transaction = models.Transaction(
        child_id=child_id,
        amount=amount,
        type="add",
        description="total"
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return {
        "message": f"Added {amount} to main account",
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

    # Kiểm tra tổng chia tiền phải đúng bằng total
    total = db_wallet.total if hasattr(db_wallet, 'total') else 0
    sum_split = sum([x for x in [savings, charity, spending, study] if x is not None])
    if sum_split != total:
        raise HTTPException(status_code=400, detail=f"Tổng chia ({sum_split}) phải đúng bằng tổng tiền ({total})")


    if savings is not None and savings > 0:
        crud.add_money_to_wallet(db, child_id, int(savings), field="savings")
        transaction = models.Transaction(
            child_id=child_id,
            amount=int(savings),
            type="add",
            description=f"saving" 
        )
        db.add(transaction)
        transactions.append(transaction)

    if charity is not None and charity > 0:
        crud.add_money_to_wallet(db, child_id, int(charity), field="charity")
        transaction = models.Transaction(
            child_id=child_id,
            amount=int(charity),
            type="add",
            description=f"charity"
        )
        db.add(transaction)
        transactions.append(transaction)

    if spending is not None and spending > 0:
        crud.add_money_to_wallet(db, child_id, int(spending), field="spending")
        transaction = models.Transaction(
            child_id=child_id,
            amount=int(spending),
            type="add",
            description=f"spending"
        )
        db.add(transaction)
        transactions.append(transaction)

    if study is not None and study > 0:
        crud.add_money_to_wallet(db, child_id, int(study), field="study")
        transaction = models.Transaction(
            child_id=child_id,
            amount=int(study),
            type="add",
            description=f"study"
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
    # Kiểm tra không chi vượt mức số dư
    db_wallet_obj = crud.get_wallet_by_child_id(db, child_id=child_id)
    if db_wallet_obj is None or not hasattr(db_wallet_obj, wallet_type):
        raise HTTPException(status_code=400, detail="Wallet not found or invalid type")
    current_balance = getattr(db_wallet_obj, wallet_type)
    if current_balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds in selected wallet")
    db_wallet = crud.spend_money(db, child_id=child_id, amount=int(amount), wallet_type=wallet_type)
    transaction = models.Transaction(
        child_id=child_id,
        amount=int(amount),
        type=f"spend",
        description= wallet_type
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