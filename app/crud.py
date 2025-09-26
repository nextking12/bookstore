from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from . import models, schemas

#combines your @Service and @Repository layers from Java.
class BookRepository:
    """Repository class for book operations combining service and data access layers."""
    # Combines BookService + BookRepository from Java
    # In Python, we often merge these layers for simpler APIs
  
def get_all_books(self, db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
        """Get all books Like: List<Book> findAll()
        Added pagination (like Spring Data's Pageable)."""
        return db.query(models.Book).offset(skip).limit(limit).all()

def get_book_by_id(self, db: Session, book_id: int) -> Optional[models.Book]:
        """Get a book by its ID."""
        return db.query(models.Book).filter(models.Book.id == book_id).first()
        # Like: public Optional<Book> findById(int id)

def get_book_by_isbn(self, db: Session, isbn: str):
        """Get a book by its ISBN."""
        return db.query(models.Book).filter(models.Book.isbn == isbn).first()

def create_book(self, db: Session, book: schemas.BookCreate):
        """Create a new book in the database."""
         # Convert Pydantic model to SQLAlchemy model
        # book.model_dump() is like BeanUtils.copyProperties()
        db_book = models.Book(**book.model_dump())

        # Add to session (like entityManager.persist())
        db.add(db_book)
         # Commit transaction (like @Transactional)
        db.commit()
        # Refresh to get the ID (like entityManager.refresh())
        db.refresh(db_book)
        return db_book

def search_books(self, db: Session, search_term: str) -> List[models.Book]:
        """Search books by title or author."""
        return db.query(models.Book).filter(
            or_(
                # ilike() is case-insensitive LIKE (PostgreSQL style)
                models.Book.title.ilike(f"%{search_term}%"),
                models.Book.author.ilike(f"%{search_term}%")
            )
        ).all()

def update_book(self, db: Session, book_id: int, book: schemas.BookUpdate) -> Optional[models.Book]:
        """Update a book by its ID

        Spring Boot equivalent:
        @PutMapping("/books/{id}")
        public ResponseEntity<Book> updateBook(@PathVariable Long id,
                                             @RequestBody BookUpdateDTO bookDto) {
            Optional<Book> optionalBook = bookRepository.findById(id);
            if (optionalBook.isPresent()) {
                Book existingBook = optionalBook.get();
                BeanUtils.copyProperties(bookDto, existingBook, getNullPropertyNames(bookDto));
                return ResponseEntity.ok(bookRepository.save(existingBook));
            }
            return ResponseEntity.notFound().build();
        }
        """
        # Find the existing book
        db_book = db.query(models.Book).filter(models.Book.id == book_id).first()

        if db_book:
            # Update only non-None fields (partial update)
            # This is like Spring's @DynamicUpdate
            book_data = book.model_dump(exclude_unset=True)  # Only include set fields
            for field, value in book_data.items():
                setattr(db_book, field, value)  # Like reflection in Java

            db.commit()
            db.refresh(db_book)
            return db_book

        return None

def delete_book(self, db: Session, book_id: int) -> bool:
        """Delete a book by its ID

        Spring Boot equivalent:
        @DeleteMapping("/books/{id}")
        public ResponseEntity<Void> deleteBook(@PathVariable Long id) {
            if (bookRepository.existsById(id)) {
                bookRepository.deleteById(id);
                return ResponseEntity.noContent().build();
            }
            return ResponseEntity.notFound().build();
        }
        """
        db_book = db.query(models.Book).filter(models.Book.id == book_id).first()

        if db_book:
            db.delete(db_book)  # Like entityManager.remove()
            db.commit()
            return True

        return False

# Create a singleton instance (like @Component in Spring)
book_repository = BookRepository()

"""
## Key Python vs Spring Boot Concepts:

### 1. Dependency Injection

• Spring Boot: @Autowired automatically injects dependencies
• Python/FastAPI: We pass db: Session explicitly to each method

### 2. Transaction Management

• Spring Boot: @Transactional handles commit/rollback automatically
• Python: We manually call db.commit() and can handle rollbacks

### 3. Data Conversion

• Spring Boot: BeanUtils.copyProperties(source, target)
• Python: **book.model_dump() spreads dictionary into constructor

### 4. Partial Updates

• Spring Boot: Custom logic to ignore null fields
• Python: exclude_unset=True only includes explicitly set fields

### 5. Query Building

• Spring Boot: @Query annotations or method naming conventions
• Python: SQLAlchemy's fluent query API

The main difference is that Python is more explicit - you see exactly what's happening with database sessions,
commits, and data conversion, while Spring Boot hides much of this behind annotations and conventions.
"""

