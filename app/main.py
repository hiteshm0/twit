from typing import Optional
from fastapi import FastAPI, status, Response, HTTPException
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    isPublished: bool = True
    Rating: Optional[int] = None

app = FastAPI()

def next_id():
    cur_id = my_posts[-1]["id"]
    return cur_id + 1

def search_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
def find_index_of_post(id):
    for i, post in enumerate(my_posts):
        if( post["id"] == id):
            return i

@app.get("/")
async def read_root():
    return {"Hello": "World"}

my_posts = [{"id" : 1, "title" : "Backend Frameworks", "content" : "My favorite backend framework is FastAPI"}]

@app.get("/posts")
def read_posts():
    return my_posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def add_post(post: Post):
    temp_post = post.model_dump()
    temp_post["id"] = next_id()
    my_posts.append(temp_post)
    return {"Message": temp_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = search_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested post not found")
    return {"post": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_of_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Requested post not found"
        )
    my_posts.pop(index)
    return None

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_of_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "Requested post not found"
        )
    
    temp_post = post.model_dump()
    temp_post["id"] = id
    my_posts[index] = temp_post
    return {"Message": "Post Updated"}





