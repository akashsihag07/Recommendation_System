"""

Application entry point.
"""

import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo.errors import ConnectionFailure

from .database import check_db
from .routers import genres, health, languages, recommend, search
from .seed import init_db
from .vectors import load_vectors

app = FastAPI(title="Movie Matcher API", version="1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health.router)
app.include_router(genres.router)
app.include_router(languages.router)
app.include_router(search.router)
app.include_router(recommend.router)


@app.on_event("startup")
def start_server():
    """Initialize the application."""
    for attempt in range(1, 11):
        try:
            check_db()
            init_db()
            load_vectors()
            return

        except ConnectionFailure:
            print(f"[startup] mongo not ready ({attempt}/10)")
            time.sleep(3)

    print("[startup] couldn't connect to mongo.")