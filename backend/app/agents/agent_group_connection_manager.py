from fastapi import WebSocket
from typing import Dict, List, Tuple

class AgentGroupConnectionManager:
    def __init__(self) -> None:
        # 
        self.active_connections: Dict[Tuple[int, int], List[WebSocket]] = {}
        
    async def connect(self, user_id: int, group_id: int, websocket: WebSocket):
        await websocket.accept()
        if (user_id, group_id) in self.active_connections:
            self.active_connections[(user_id, group_id)].append(websocket)
        else:
            self.active_connections[(user_id, group_id)] = [websocket]
            
    def disconnect(self, user_id: int, group_id: int, websocket: WebSocket):
        self.active_connections[(user_id, group_id)].remove(websocket)
        if not self.active_connections[(user_id, group_id)]:
            del self.active_connections[(user_id, group_id)]
            
    async def send_message_to_client(self, message: Dict, client_websocket: WebSocket):
        await client_websocket.send_json(message)
                
    async def broadcast(self, message: Dict):
        for connections in self.active_connections.values():
            for connection in connections:
                await connection.send_json(message)