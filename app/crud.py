from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from . import models, schemas

#combines your @Service and @Repository layers from Java.
class BookRepository:
    #Combines BookService + BookRepository from Java
    #In Python, we often merge these layers for simpler APIs
 def get_book_by_id(self, db: Session, book_id: int) -> Optional[models.Book]:    
    return db.query(models.Book).filter(models.Book.id == book_id).first()
    #Like: public Optional<Book> findById(int id)
def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book) 