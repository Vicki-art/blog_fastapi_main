from fastapi import  Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import  get_db
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func

router = APIRouter(prefix = "/posts",
                   tags = ["Posts"])


@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user), skip: int = 0, search: Optional[str] = ''):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                         models.Vote.post_id == models.Post.id,
                                         isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).offset(skip).all()
    return posts


@router.post("/", status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(new_post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    print('user_id')
    created_post = models.Post(owner_id = current_user.id, **new_post.dict())
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,
             db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                         models.Vote.post_id == models.Post.id,
                                         isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id {id} was not found" )

    return post


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = post_query.first()

    if not deleted_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post with id {id} does not exist")


    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")

    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int,
                post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session = False)
    db.commit()
    return post_query.first()
