import uuid
import bcrypt
import PyJWT as jwt  # Changed from 'import jwt' to 'import PyJWT as jwt'
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from pydantic_schemas.user_create import UserCreate
from pydantic_schemas.user_login import UserLogin
from middleware.auth_middleware import auth_middleware
from models.favorite import Favorite
from sqlalchemy.orm import joinedload
from models.media import Media  # or from your correct models file path



router = APIRouter()

# Register a new user
@router.post("/signup", status_code=201)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(400, "This email already exists")

    # Hash password before saving
    hashed_pw = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    user_db = User(
        id=str(uuid.uuid4()),
        name=user.name,
        email=user.email,
        password=hashed_pw
    )

    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return user_db

# Login user and return token
@router.post('/login')
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    user_db = db.query(User).filter(User.email == user.email).first()
    if not user_db:
        raise HTTPException(400, "User with this email doesn't exist")

    if not bcrypt.checkpw(user.password.encode(), user_db.password):
        raise HTTPException(400, "Incorrect Password")

    token = jwt.encode({'id': user_db.id}, 'password_key', algorithm='HS256')

    return {'token': token, 'user': user_db}

# Protected route to fetch current user info
@router.get('/me')
def current_user_data(db: Session = Depends(get_db), user_dict=Depends(auth_middleware)):
    user = db.query(User).filter(User.id == user_dict['uid']).first()
    if not user:
        raise HTTPException(404, "User not found")

    return {"user": user}


@router.get("/me/details")
def get_user_details(
    db: Session = Depends(get_db), 
    auth_dict = Depends(auth_middleware)
):
    user_id = auth_dict['uid']
    
    # Get user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    # Get favorited media
    favorites = db.query(Favorite).filter(Favorite.user_id == user_id).options(
        joinedload(Favorite.media)
    ).all()
    
    saved_media = []
    for fav in favorites:
        media = fav.media
        saved_media.append({
            "media_id": media.id,
            "media_url": media.media_url,
            "description": media.description,
            "created_at": media.created_at
        })

    # Get uploaded media IDs
    uploaded_media_ids = db.query(Media.id).filter(Media.user_id == user_id).all()
    uploaded_media_ids = [mid[0] for mid in uploaded_media_ids]

    return {
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        },
        "saved_media": saved_media,
        "uploaded_media_ids": uploaded_media_ids
    }