from typing import Optional
from fastapi import FastAPI, status, Response, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class Post(BaseModel):
    title: str
    content: str
    isPublished: bool = True
    Rating: Optional[int] = None

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(database="fastapifccc_db", user="hiteshm", password="", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was successful")
        break
    except Exception as error:
        print(f"Connection failed with error: {error}")

@app.get("/")
async def read_root():
    return {"Hello": "World"}

my_posts = [{"id" : 1, "title" : "Backend Frameworks", "content" : "My favorite backend framework is FastAPI"}]

@app.get("/posts")
def read_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def add_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, "isPublished") VALUES (%s,%s,%s) RETURNING *""",
                   (post.title, post.content, post.isPublished))
    temp_post = cursor.fetchone()
    conn.commit()
    return {"Message": temp_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Requested post not found"
        )
    return {"post": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    post = cursor.fetchone()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Requested post not found"
        )
    conn.commit()
    return None

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, "isPublished" = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.isPublished, str(id))
                   )
    temp_post = cursor.fetchone()
    if temp_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Requested post not found"
        )
    conn.commit()
    return {"Updated": temp_post}





