from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session

from ..database import get_db
from ..crud import book_repository
from .. import schemas

from typing import List

# Create router - like @RestController + @RequestMapping("/books")
router = APIRouter(
    prefix="/books",  # All routes will start with /books
    tags=["books"],   # Groups endpoints in OpenAPI docs - like @Api(tags = "Books")
    responses={404: {"description": "Not found"}}
)

# GET /books - Get all books with pagination
@router.get("/", response_model=List[schemas.BookResponse])
def get_books(
    skip: int = 0,  # Like @RequestParam(defaultValue = "0") int page
    limit: int = 100,  # Like @RequestParam(defaultValue = "100") int size
    db: Session = Depends(get_db)  # Like @Autowired EntityManager em
):
    books = book_repository.get_all_books(db, skip=skip, limit=limit)
    return books

# GET /books/{book_id} - Get single book by ID
@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(
    book_id: int,  # Like @PathVariable Long bookId
    db: Session = Depends(get_db)
):
    book = book_repository.get_book_by_id(db, book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return book

# POST /books - Create a new book
@router.post("/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: schemas.BookCreate,  # Like @RequestBody @Valid BookCreateDTO
    db: Session = Depends(get_db)
):
    """
    Create a new book

    Spring Boot equivalent:
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public BookDTO createBook(@RequestBody @Valid BookCreateDTO bookDto)
    """
    # Check if ISBN already exists (business logic validation)
    if book.isbn:
        existing_book = book_repository.get_book_by_isbn(db, isbn=book.isbn)
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book with ISBN {book.isbn} already exists"
            )

    return book_repository.create_book(db=db, book=book)

# PUT /books/{book_id} - Update a book
@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int,  # Like @PathVariable Long id
    book: schemas.BookUpdate,  # Like @RequestBody BookUpdateDTO
    db: Session = Depends(get_db)
):
    """
    Update an existing book

    Spring Boot equivalent:
    @PutMapping("/{id}")
    public ResponseEntity<BookDTO> updateBook(
        @PathVariable Long id,
        @RequestBody BookUpdateDTO bookDto
    )
    """
    updated_book = book_repository.update_book(db, book_id=book_id, book=book)
    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    return updated_book

# DELETE /books/{book_id} - Delete a book
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,  # Like @PathVariable Long id
    db: Session = Depends(get_db)
):
    """
    Delete a book

    Spring Boot equivalent:
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public ResponseEntity<Void> deleteBook(@PathVariable Long id)
    """
    success = book_repository.delete_book(db, book_id=book_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found"
        )
    # FastAPI automatically returns 204 No Content for None return
    return None
# GET /books/search?q=term - Search books
@router.get("/search", response_model=List[schemas.BookResponse])
def search_books(
    q: str,  # Like @RequestParam String query
    db: Session = Depends(get_db)
):
    """
    Search books by title or author

    Spring Boot equivalent:
    @GetMapping("/search")
    public List<BookDTO> searchBooks(@RequestParam String q)
    """
    if len(q.strip()) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query must be at least 2 characters long"
        )

    return book_repository.search_books(db, search_term=q)

# GET /books/isbn/{isbn} - Get book by ISBN
@router.get("/isbn/{isbn}", response_model=schemas.BookResponse)
def get_book_by_isbn(
    isbn: str,  # Like @PathVariable String isbn
    db: Session = Depends(get_db)
):
    """
    Get a book by its ISBN

    Spring Boot equivalent:
    @GetMapping("/isbn/{isbn}")
    public ResponseEntity<BookDTO> getBookByIsbn(@PathVariable String isbn)
    """
    book = book_repository.get_book_by_isbn(db, isbn=isbn)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ISBN {isbn} not found"
        )
    return book

# GET /books/stats - Get book statistics (bonus endpoint)
@router.get("/stats")
def get_book_stats(db: Session = Depends(get_db)):
    """
    Get basic statistics about books

    Spring Boot equivalent:
    @GetMapping("/stats")
    public BookStatsDTO getBookStats()
    """
    total_books = len(book_repository.get_all_books(db, skip=0, limit=10000))

    return {
        "total_books": total_books,
        "message": f"Database contains {total_books} books"
    }


"""
## Key Routing Concepts Explained:

### 1. Router Prefix

router = APIRouter(prefix="/books")
# When included with app.include_router(books.router, prefix="/api")
# Final URLs: /api/books/, /api/books/{id}, etc.

### 2. Route Order Matters

@router.get("/search")      # Must come BEFORE /{book_id}
@router.get("/{book_id}")   # This would catch "/search" if placed first

### 3. HTTP Methods & Status Codes

@router.post("/", status_code=201)   # Like @PostMapping + @ResponseStatus
@router.delete("/", status_code=204) # Like @DeleteMapping + 204 No Content

### 4. Error Handling

raise HTTPException(status_code=404, detail="Not found")
# Like: throw new ResponseStatusException(HttpStatus.NOT_FOUND, "Not found")

### 5. Documentation Tags

tags=["books"]  # Groups endpoints in Swagger UI
# Like Swagger's @Api(tags = "Book Management")

## Final URL Structure:

• GET /api/books/ → List all books
• GET /api/books/123 → Get book by ID
• POST /api/books/ → Create book
• PUT /api/books/123 → Update book
• DELETE /api/books/123 → Delete book
• GET /api/books/search?q=python → Search books
• GET /api/books/isbn/9781234567890 → Get by ISBN
• GET /api/books/stats → Get statistics


"""



