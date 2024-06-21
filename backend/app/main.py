from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.endpoints import user, post, chat
from app.websocket.connection_manager import ConnectionManager

from app.api.endpoints.agents.admin import agent as admin_ai_agent, agent_group as admin_agent_group, agent_group_member as admin_agent_group_member, agent_group_message as admin_agent_group_message
from app.api.endpoints.agents.user import agent as user_ai_agent, agent_group as user_agent_group, agent_group_member as user_agent_group_member, agent_group_message as user_agent_group_message

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

# Test basic routes
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(post.router, prefix="/posts", tags=["posts"])
app.include_router(chat.router, prefix="/chat", tags=["chat"]) # websocket and RESTful

# Agent API routes
## admin routes
app.include_router(admin_ai_agent.router, prefix="/ai_agents/admin/agents", tags=["Admin AI Agents"])
app.include_router(admin_agent_group.router, prefix="/ai_agents/admin/agent_groups", tags=["Admin Agent Groups"])
app.include_router(admin_agent_group_member.router, prefix="/ai_agents/admin/agent_groups/{group_id}/members", tags=["Admin Agent Group Members"])
app.include_router(admin_agent_group_message.router, prefix="/ai_agents/admin/agent_groups/{group_id}/messages", tags=["Admin Agent Group Messages"])

# user routes
app.include_router(user_ai_agent.router, prefix="/ai_agents/users/{user_id}/agents", tags=["User AI Agents"])
app.include_router(user_agent_group.router, prefix="/ai_agents/users/{user_id}/agent_groups", tags=["User Agent Groups"])
app.include_router(user_agent_group_member.router, prefix="/ai_agents/users/{user_id}/agent_groups/{group_id}/members", tags=["User Agent Group Members"])
app.include_router(user_agent_group_message.router, prefix="/ai_agents/users/{user_id}/agent_groups/{group_id}/messages", tags=["User Agent Group Messages"])







# To run the app for dev
## use bash `uvicorn app.main:app --reload`
