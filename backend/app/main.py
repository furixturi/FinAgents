import asyncio, uvicorn
from fastapi import FastAPI
from app.api.endpoints import user
from app.api.endpoints import post
# from app.websocket.endpoint import websocket_endpoint
from app.db import init_db

# Initialize/sync DB at startup
async def lifespan(app: FastAPI):
    # at start up
    await init_db()
    yield
    # at shutdown

app = FastAPI(lifespan=lifespan)

# Include routes
# app.include_router(user.router, prefix="/users", tags=["users"])
# app.include_router(post.router, prefix="/posts", tags=["posts"])

# WebSocket route
# app.add_api_websocket_route("/ws/posts/{user_id}", websocket_endpoint)


# To run the app
## use bash `uvicorn app.main:app --reload`
