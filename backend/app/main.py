import asyncio, uvicorn
from fastapi import FastAPI
from app.api.endpoints import user
from app.api.endpoints import post
from app.websocket.endpoint import websocket_endpoint
from app.db import init_db

app = FastAPI()

# Include routes
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(post.router, prefix="/posts", tags=["posts"])

# WebSocket route
app.add_api_websocket_route("/ws/posts/{user_id}", websocket_endpoint)

# Initialize DB and run the application
if __name__ == "__main__":
    asyncio.run(init_db())
    
    # dev
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True) 