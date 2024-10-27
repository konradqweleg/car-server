from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

# Zarządzanie połączeniami klientów
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data: bytes):
        # Wysyła binarne dane (obraz JPEG) do wszystkich połączonych klientów
        for connection in self.active_connections:
            await connection.send_bytes(data)

manager = ConnectionManager()

# Endpoint WebSocket do odbierania i przesyłania obrazów
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Odbiera dane binarne (JPEG) od klienta
            data = await websocket.receive_bytes()
            # Wysyła obraz JPEG do wszystkich pozostałych połączonych klientów
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
