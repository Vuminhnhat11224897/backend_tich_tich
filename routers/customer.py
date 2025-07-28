from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import crud
import schemas
from database import get_db

router = APIRouter(
    prefix="/customers",
    tags=["customers"]
)

@router.post("/", response_model=schemas.CustomerResponse)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_phone(db, phone=customer.phone)
    if db_customer:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    # Truyền đúng tham số cho CRUD
    return crud.create_customer(db=db, name=customer.name, phone=customer.phone, pin=customer.pin)

# Endpoint reset pin (quên mật khẩu)
@router.put("/reset-pin/{user_id}")
def reset_pin(user_id: int, new_pin: str = Body(..., embed=True), db: Session = Depends(get_db)):
    success = crud.update_pin_by_user_id(db, user_id=user_id, new_pin=new_pin)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "Pin updated successfully"}

@router.get("/phone/{phone}", response_model=schemas.CustomerResponse)
def read_customer_by_phone(phone: str, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_phone(db, phone=phone)
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer