from .. import models, oauth2, schemas
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import engine, get_db
from sqlalchemy import and_, func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)
# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p
#     return None

# def del_post(id):
#     for p in my_posts:
#         print(p["id"], id)
#         if p["id"] == id:
#             print("found post")
#             my_posts.remove(p)
#             return True
#     return None

# def post_index(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return my_posts.index(p)
#     return None

@router.get("/test")
async def test():
    return {"message": "this is a test"}

@router.get("/", response_model = List[schemas.Post])
async def get_posts(db: Session = Depends(get_db)):
    # posts = cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()
    return posts

# @router.post("/create_post")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title {payload['title']} content: {payload['content']} "} 

@router.get("/personal", response_model=List[schemas.PostOut])
def get_my_posts(db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user),
                 limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    print(limit)
    # posts = db.query(models.Post).filter(and_(models.Post.owner_id == current_user.id, models.Post.title.contains(search))).limit(limit).offset(skip).all()
    # if not posts:
    #     raise HTTPException(status_code=404, detail="no posts found")
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(and_(models.Post.owner_id == current_user.id, models.Post.title.contains(search))).limit(limit).offset(skip).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
#                    (post.title, post.content, post.published))
#     new_post = cursor.fetchone()

# # make sure to commit changes whenever you insert sth new into the database
#     conn.commit()
    
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/latest")
def get_latest_post(db: Session = Depends(get_db)):
    latest = db.query(models.Post).order_by(models.Post.id.desc()).first()
    if not latest:
        raise HTTPException(status_code=404, detail=f"no posts available")
    return latest

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return post

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")

    # return {"data": post}

    # post = find_post(str(id))
    # if post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {"message": f"post with id {id} was not found"}
    # return {"post_detail": post}

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # result = del_post(id)
    # print(id, result)
 
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # result = cursor.fetchone()
    # conn.commit()

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="not authorized to perform requested action")

    print(post)
    post_query.delete(synchronize_session = False)
    db.commit()

    # print(my_posts)

    response.headers["X-Message"] = "Post successfully deleted."
    return Response(status_code=status.HTTP_204_NO_CONTENT, )


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostBase, db: Session = Depends(get_db), current_user: int  = Depends(oauth2.get_current_user)):
    # index = post_index(id)
    # print(index)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    # my_posts[index] = post.model_dump() 
    # my_posts[index]["id"] = id
    # print(my_posts)

    # cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (post.title, post.content, str(id)))
    # post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    found_post = post_query.first()

    if found_post == None:
        raise HTTPException(status_code=404, detail=f"post with id {id} was not found")
    
    if found_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="not authorized to perform requested action")
    post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()
    return post_query.first()