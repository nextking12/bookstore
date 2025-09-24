from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()# Base class for all models - like extending JpaRepository

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)

    author = Column(String(100), nullable=False)

    isbn = Column(String(13), unique=True, nullable=True)

    published_year = Column(Integer, nullable=True)


    ## Key Concepts Explained:
"""
1. Base = declarative_base() - Like your base entity class that all entities extend
2. __tablename__ = "books" - Like @Table(name="books")
3. Column(Integer, primary_key=True) - Like @Id @GeneratedValue
4. nullable=False - Like @Column(nullable=false)
5. unique=True - Like @Column(unique=true)

## What This Creates:

When the app starts, this will create a table:

CREATE TABLE books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    isbn VARCHAR(13) UNIQUE,
    published_year INTEGER
);
"""