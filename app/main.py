from fastapi import FastAPI
from .database import Base, engine
from .routers import post, user, vote
from . import auth, oauth2

#Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(oauth2.router)
app.include_router(vote.router)



