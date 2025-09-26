from fastapi import FastAPI

from .database import create_tables
from .routers import books  # Import the books router

# Create FastAPI app - like @SpringBootApplication
app = FastAPI(
    title="Bookstore API",
    description="A simple bookstore API built with FastAPI",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI at /docs
    redoc_url="/redoc"  # ReDoc at /redoc
)

# Include routers - like @ComponentScan or @Import
app.include_router(books.router, prefix="/api")

# Create database tables on startup - like @PostConstruct
@app.on_event("startup")
def startup_event():
    """
    Run when application starts
    Like: @EventListener(ApplicationReadyEvent.class)
    """
    create_tables()

# Health check endpoints
@app.get("/")
async def root():
    """
    Root endpoint - basic health check
    Like: @GetMapping("/")
    """
    return {
        "message": "Bookstore API is running!",
        "version": "1.0.0",
        "docs": "/docs",
        "books_api": "/api/books"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    Like: @GetMapping("/actuator/health") in Spring Boot Actuator
    """
    return {
        "status": "healthy",
        "service": "bookstore-api"
    }



# Keep your original hello endpoint for learning purposes
@app.get("/hello/{name}")
async def say_hello(name: str):
    """Simple hello endpoint for testing"""
    return {"message": f"Hello {name}"}


