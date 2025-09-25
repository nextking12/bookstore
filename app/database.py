from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base


#This is like your application.properties + @Configuration for DataSource

DATABASE_URL = "sqlite:///./library.db"# Like: spring.datasource.url=jdbc:sqlite:./library.db

# Create database engine - like @Bean DataSource
# echo=True shows SQL queries in console (like spring.jpa.show-sql=true)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite specific
    echo=True  # This shows SQL queries in console - great for learning!
)

# Session factory - like EntityManagerFactory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency function - like @Autowired EntityManager
def get_db():
    """
    Provides database session to each request
    Like: @Autowired private EntityManager entityManager;
    """
    db = SessionLocal()
    try:
        yield db  # Dependency injection
    finally:
        db.close()  # Auto-cleanup

# Create all tables - like @EnableJpaRepositories + ddl-auto=create
def create_tables():
    """
    Creates all tables defined in models
    Like: spring.jpa.hibernate.ddl-auto=create-drop
    """
    Base.metadata.create_all(bind=engine)

    """
    ## Key Concepts:

1. create_engine(DATABASE_URL) - Like configuring your DataSource
2. SessionLocal = sessionmaker(...) - Template for database sessions
3. get_db() - Dependency injection function (like @Autowired)
4. Base.metadata.create_all() - Creates tables from your models

## What This Does:

• Creates a SQLite database file called library.db
• Sets up connection pooling
• Provides session management
• Will create the books table based on your Book model
    """