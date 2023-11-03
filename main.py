from fastapi import FastAPI
from fastapi.params import Body
from typing import List
from fastapi import Depends
from .import models
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import post
from pydantic import BaseModel
from sqlalchemy import insert




models.Base.metadata.create_all(bind=engine)
app = FastAPI()

from pydantic import BaseModel

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    hashed_password:str
    published:bool =True



#sending any api request we use this:db:session=depends(get_db)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/sqlalchemy")
def test_post(db:Session=Depends(get_db)):
    posts=db.query(models.post).all()
    return {'status':posts}


@app.get("/posts")
def root(db:Session=Depends(get_db)):
    posts=db.query(models.post).all()
    return {"status":posts}


@app.post("/posts")
def create_post(posts:PostResponse, db:Session=Depends(get_db)):
   new_posts= models.post(title=post.title,content=post.content,hashed_password=post.hashed_password,published=post.published)
   db.add(new_posts)
   db.commit()
   db.refresh(new_posts)
   return {"message":new_posts}