from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


general_clients: List[WebSocket] = []
driver_clients: List[WebSocket] = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    general_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_bytes()
            for client in general_clients:
                if client != websocket:
                    await client.send_bytes(data)
    except WebSocketDisconnect:
        general_clients.remove(websocket)

@app.websocket("/check-ip")
async def client_check_server_ip(websocket: WebSocket):
    await websocket.accept()
    client_ip = websocket.client[0]
    response_message = f"Your client IP address is: {client_ip}"
    await websocket.send_text(response_message)
    await websocket.close()

@app.websocket("/driver")
async def driver(websocket: WebSocket):
    await websocket.accept()
    driver_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Otrzymano polecenie: {data}")

            for client in driver_clients:
                if client != websocket:
                    await client.send_text(data)
    except WebSocketDisconnect:
        driver_clients.remove(websocket)

@app.websocket("/banan")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    general_clients.append(websocket)
    try:
        while True:

            data = await websocket.receive_bytes()

            filename = f"imageBanan.jpeg"
            with open(filename, "wb") as f:
                f.write(data)


            for client in general_clients:
                if client != websocket:
                    await client.send_bytes(data)
    except WebSocketDisconnect:
        general_clients.remove(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
