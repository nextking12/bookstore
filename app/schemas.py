from pydantic import BaseModel, Field
from typing import Optional

class BookBase (BaseModel):
  #  Base schema with common fields
    #Like your base DTO class in Java
    
    title : str = Field(..., min_length=1, max_length=200, description = "Book Title")
    author: str = Field(..., min_length=1, max_length=100, description = "Book Author")
    isbn :  Optional[str] = Field(None, min_length=10, max_length=13, description= "ISBN Number")
    published_year: Optional[int] = Field(None, ge=1000, le=2030, description = "Year Published")

class BookCreate(BookBase):
  #  Schema for creating a book (POST requests)
  #  Like: @RequestBody BookCreateDTO
    #All fields from BookBase are required (except Optional ones)
   pass

class BookUpdate(BookBase):
   #Schema for updating a book (PUT requests)
    #Like: @RequestBody BookUpdateDTO
    #All fields are optional for partial updates
    title: Optional[str] = Field(None, min_length=1, max_length=200, description = "Book Title")
    author: Optional[str] = Field(None, min_length=1, max_length=100, description = "Book Author")
    isbn: Optional[str] = Field(None, min_length=10, max_length=13, description= "ISBN Number")
    published_year: Optional[int] = Field(None, ge=1000, le=2030, description = "Year Published")

class BookResponse  (BookBase):
    #Schema for returning a book (GET requests)
    #Like: @ResponseBody BookDTO
    #Includes id from Book model
    id: int

    class Config:
        from_attributes = True # Like @JsonFormat(shape=JsonFormat.Shape.STRING)  # Converts SQLAlchemy model to Pydantic automatically

## Key Concepts:
"""
1. BookBase - Common fields with validation rules
2. BookCreate - For POST requests (like @RequestBody in Java)
3. BookUpdate - For PUT requests with optional fields
4. BookResponse - For responses, includes the database ID
5. Field(...) - Validation rules (like Bean Validation annotations)

## Validation Mapping:

Field(..., min_length=1)          # @NotEmpty @Size(min=1)
Field(None, ge=1000, le=2030)     # @Min(1000) @Max(2030)
Optional[str]                     # Field can be null/None

## The Data Flow:

POST JSON → BookCreate → Book Model → Database
Database → Book Model → BookResponse → JSON Response
"""