import os

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from src.routes.user import user_router
from src.routes.posts import post_router
from src.database.engine import Postgres
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    docs_url="/api/docs",
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
)

app.state.postgres = Postgres.create(url=os.getenv("DB_URL"))
app.include_router(user_router)
app.include_router(post_router)
