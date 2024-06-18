from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[int, List[WebSocket]] = {}
        
    async def connect(self, connection_id: int, websocket: WebSocket):
        await websocket.accept()
        if connection_id in self.active_connections:
            self.active_connections[connection_id].append(websocket)
        else:
            self.active_connections[connection_id] = [websocket]
            
    def disconnect(self, connection_id: int, websocket: WebSocket):
        self.active_connections[connection_id].remove(websocket)
        if not self.active_connections[connection_id]:
            del self.active_connections[connection_id]
            
    async def send_personal_message(self, message: Dict, websocket: WebSocket):
        await websocket.send_json(message)
                
    async def broadcast(self, message: Dict):
        for connections in self.active_connections.values():
            for connection in connections:
                await connection.send_json(message)