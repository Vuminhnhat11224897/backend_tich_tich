from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import crud
import schemas
from database import get_db
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

@router.post("/", response_model=schemas.CustomerResponse)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    if not customer.phone or len(customer.phone) < 10:
        raise HTTPException(status_code=400, detail="Phone number must be at least 10 digits")
    db_customer = crud.get_customer_by_phone(db, phone=customer.phone)
    if db_customer:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    customer.phone = customer.phone[:4] + "***" + customer.phone[-3:]
    return crud.create_customer(db=db, name=customer.name, phone=customer.phone)


@router.get("/phone/{phone}", response_model=schemas.CustomerResponse)
def read_customer_by_phone(phone: str, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_phone(db, phone=phone)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer




