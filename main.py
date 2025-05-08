from fastapi import FastAPI
from models.base import Base
from routes import auth, media
from database import engine, get_db

app = FastAPI()
application = app

# Register routes
app.include_router(auth.router, prefix='/auth')
app.include_router(media.router, prefix='/media')

# Create database tables automatically
Base.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"status": "API is running"}