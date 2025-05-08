from fastapi import FastAPI
from models.base import Base
from routes import auth, media  # Added media routes
from database import engine, get_db

app = FastAPI()

# Register routes
app.include_router(auth.router, prefix='/auth')
app.include_router(media.router, prefix='/media')  # Added media routes

# Create database tables automatically
Base.metadata.create_all(engine)
