from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.category import CategoryService


def get_category_service(db: Session = Depends(get_db)):
    return CategoryService(db)
