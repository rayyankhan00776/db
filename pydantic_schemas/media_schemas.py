from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MediaComment(BaseModel):
    media_id: str
    comment: str

class MediaLike(BaseModel):
    media_id: str

class MediaFavorite(BaseModel):
    media_id: str

class CommentResponse(BaseModel):
    id: str
    media_id: str
    user_id: str
    text: str
    created_at: datetime

class MediaResponse(BaseModel):
    id: str
    media_url: str
    description: Optional[str] = None
    user_id: str
    created_at: datetime
    like_count: int = 0
    comment_count: int = 0
    is_liked: bool = False
    is_favorited: bool = False