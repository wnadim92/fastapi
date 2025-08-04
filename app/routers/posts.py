from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from .. database import engine, get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/api/v1/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostOut]) 
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("vote")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return [{"Post": post, "votes": votes} for post, votes in results]

@router.get("/latest", response_model=schemas.Post)
def latest_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.published == True).order_by(models.Post.created_at.desc()).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return post

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first() 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")        
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post,)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *  """, (post.title, post.content, post.published))
    #post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *  """, (str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(updated_post:schemas.PostCreate, id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *  """, (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()  
    return post_query.first()