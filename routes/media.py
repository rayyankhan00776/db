import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from middleware.auth_middleware import auth_middleware
import cloudinary
import cloudinary.uploader
from models.media import Media
from models.comment import Comment
from models.like import Like
from models.favorite import Favorite
from pydantic_schemas.media_schemas import MediaComment, MediaLike, MediaFavorite
from typing import Optional
from models.user import User


router = APIRouter()

# Configure Cloudinary
cloudinary.config( 
    cloud_name = "diqoy7rc4", 
    api_key = "683212584585384", 
    api_secret = "LZWJKJnReDXhMC2jlb272RouMCw",
    secure=True
)

@router.post("/upload", status_code=201)
def upload_media(
    image: UploadFile = File(...), 
    description: str = Form(...),
    db: Session = Depends(get_db),
    auth_dict = Depends(auth_middleware)
):
    media_id = str(uuid.uuid4())
    user_id = auth_dict['uid']
    
    # Upload to Cloudinary
    media_res = cloudinary.uploader.upload(
        image.file, 
        resource_type='image', 
        folder=f"media/{user_id}/{media_id}"
    )
    
    # Save to database
    new_media = Media(
        id=media_id,
        media_url=media_res['url'],
        public_id=media_res['public_id'],
        description=description,
        user_id=user_id
    )
    
    db.add(new_media)
    db.commit()
    db.refresh(new_media)
    
    return new_media

@router.get("/feed")
def get_feed(
    db: Session = Depends(get_db),
    auth_dict = Depends(auth_middleware),
    skip: int = 0,
    limit: int = 20
):
    user_id = auth_dict['uid']
    
    media_items = db.query(Media).options(joinedload(Media.user)).offset(skip).limit(limit).all()
    
    result = []
    for media in media_items:
        like_count = db.query(Like).filter(Like.media_id == media.id).count()
        is_liked = db.query(Like).filter(Like.media_id == media.id, Like.user_id == user_id).first() is not None
        is_favorited = db.query(Favorite).filter(Favorite.media_id == media.id, Favorite.user_id == user_id).first() is not None
        comment_count = db.query(Comment).filter(Comment.media_id == media.id).count()
        
        media_dict = {
            "id": media.id,
            "media_url": media.media_url,
            "description": media.description,
            "user_id": media.user_id,
            "username": media.user.name if media.user else None,
            "created_at": media.created_at,
            "like_count": like_count,
            "comment_count": comment_count,
            "is_liked": is_liked,
            "is_favorited": is_favorited
        }
        result.append(media_dict)
    
    return result

@router.post("/like")
def like_media(
    media_data: MediaLike,
    db: Session = Depends(get_db),
    auth_dict = Depends(auth_middleware)
):
    user_id = auth_dict['uid']
    
    # Check if already liked
    existing_like = db.query(Like).filter(
        Like.media_id == media_data.media_id,
        Like.user_id == user_id
    ).first()
    
    if existing_like:
        # Unlike if already liked
        db.delete(existing_like)
        db.commit()
        return {"liked": False}
    
    # Add new like
    new_like = Like(
        id=str(uuid.uuid4()),
        media_id=media_data.media_id,
        user_id=user_id
    )
    
    db.add(new_like)
    db.commit()
    
    return {"liked": True}

@router.post("/comment")
def comment_media(
    comment_data: MediaComment,
    db: Session = Depends(get_db),
    auth_dict = Depends(auth_middleware)
):
    user_id = auth_dict['uid']
    
    # Add new comment
    new_comment = Comment(
        id=str(uuid.uuid4()),
        media_id=comment_data.media_id,
        user_id=user_id,
        text=comment_data.comment
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment

@router.get("/comments/{media_id}")
def get_comments(
    media_id: str,
    db: Session = Depends(get_db),
    auth_dict = Depends(auth_middleware)
):
    # Get comments with user info
    comments = db.query(Comment).join(User).add_columns(User.name).filter(Comment.media_id == media_id).order_by(Comment.created_at.desc()).all()
    
    result = []
    for comment, username in comments:
        comment_dict = {
            "id": comment.id,
            "media_id": comment.media_id,
            "user_id": comment.user_id,
            "text": comment.text,
            "created_at": comment.created_at,
            "username": username
        }
        result.append(comment_dict)
    
    return result

@router.post("/favorite")
def favorite_media(
    favorite_data: MediaFavorite,
    db: Session = Depends(get_db),
    auth_dict = Depends(auth_middleware)
):
    user_id = auth_dict['uid']
    
    # Check if already favorited
    existing_favorite = db.query(Favorite).filter(
        Favorite.media_id == favorite_data.media_id,
        Favorite.user_id == user_id
    ).first()
    
    if existing_favorite:
        # Remove from favorites
        db.delete(existing_favorite)
        db.commit()
        return {"favorited": False}
    
    # Add to favorites
    new_favorite = Favorite(
        id=str(uuid.uuid4()),
        media_id=favorite_data.media_id,
        user_id=user_id
    )
    
    db.add(new_favorite)
    db.commit()
    
    return {"favorited": True}

@router.get("/favorites")
def get_favorites(
    db: Session = Depends(get_db),
    auth_dict = Depends(auth_middleware)
):
    user_id = auth_dict['uid']
    
    # Get favorites with media details
    favorites = db.query(Favorite).filter(
        Favorite.user_id == user_id
    ).options(
        joinedload(Favorite.media)
    ).all()
    
    return favorites

@router.get("/user/{user_id}")
def get_user_media(
    user_id: str,
    db: Session = Depends(get_db),
    auth_dict = Depends(auth_middleware),
    skip: int = 0,
    limit: int = 20
):
    # Get media for a specific user
    media_items = db.query(Media).filter(
        Media.user_id == user_id
    ).order_by(Media.created_at.desc()).offset(skip).limit(limit).all()
    
    return media_items

@router.get("/my")
def get_my_media(
    db: Session = Depends(get_db),
    auth_dict = Depends(auth_middleware),
    skip: int = 0,
    limit: int = 20
):
    user_id = auth_dict['uid']
    
    # Get media for the current user
    media_items = db.query(Media).filter(
        Media.user_id == user_id
    ).order_by(Media.created_at.desc()).offset(skip).limit(limit).all()
    
    return media_items