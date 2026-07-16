"""
Application entry point.

Wires up CORS, mounts the routers, and runs the startup sequence.
Nothing here does any recommendation work, that lives in recommender.
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


# Open CORS because the frontend runs on a different port in the same
# compose network. Would be a real origin list if this were public.
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
    """
    Connect to mongo, seed if needed, load the vectors into memory.

    Retries bcz compose starts the containers together and mongo is
    usually still coming up when this first runs. depends_on only waits
    for the container, not for mongo to accept connections.
    """
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