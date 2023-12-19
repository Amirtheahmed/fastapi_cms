#!/usr/bin/env python3.10
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

from app.routers import article, user, auth, category

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(article.router)
app.include_router(user.router)
app.include_router(category.router)


# Routes
@app.get("/")
async def root():
    return {"Hello World!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
