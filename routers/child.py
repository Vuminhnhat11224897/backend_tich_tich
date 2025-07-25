from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db

router = APIRouter(
    prefix="/children",
    tags=["children"]
)

@router.post("/", response_model=schemas.ChildResponse)
def create_child(child: schemas.ChildCreate, db: Session = Depends(get_db)):
    db_customer = crud.get_customer_by_id(db, user_id=child.parent_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Parent not found")
    return crud.create_child(db=db, child=child)

@router.get("/{parent_id}", response_model=List[schemas.ChildWithWallet])
def read_children_by_parent(parent_id: int, db: Session = Depends(get_db)):
    children = crud.get_children_by_parent(db, parent_id=parent_id)
    return children