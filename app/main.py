from fastapi import FastAPI, status
from . import models
from .database import engine
from .routes import posts, users, auth, votes
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get('/', status_code=status.HTTP_201_CREATED)
def main():
    return {"Message": "Hello, world"}


