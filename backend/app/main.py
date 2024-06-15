from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import user, post, chat
from app.connection_manager import ConnectionManager

# from app.websocket.endpoint import websocket_endpoint
from app.db import init_db, engine



# Initialize/sync DB at startup
async def lifespan(app: FastAPI):
    # at start up: initialize DB
    await init_db()
    yield
    # at shutdown: Dispose of the DB engine to clean up resources
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# Include routes
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])




# To run the app for dev
## use bash `uvicorn app.main:app --reload`
