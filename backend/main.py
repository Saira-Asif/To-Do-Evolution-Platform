from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import os
from database import create_db_and_tables
from routes import auth, tasks


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan event handler for the FastAPI application.
    Runs startup and shutdown events.
    """
    # Startup: Create database tables
    create_db_and_tables()
    yield
    # Shutdown: Cleanup code would go here if needed


# Create FastAPI app instance
app = FastAPI(
    title="Todo Web Application API",
    description="API for the Todo Web Application with Authentication",
    version="1.0.0",
    lifespan=lifespan
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the auth and tasks routes
app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")


@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Welcome to the Todo Web Application API"}


@app.get("/health")
def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )