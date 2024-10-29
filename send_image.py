import asyncio
import websockets

async def send_image(file_path: str):
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        with open(file_path, "rb") as image_file:
            image_data = image_file.read()
            await websocket.send(image_data)
            print(f"Wysłano obraz '{file_path}' do serwera.")

async def send_command(command: str):
    # Adres serwera WebSocket
    uri = "ws://localhost:8000/driver"
    async with websockets.connect(uri) as websocket:
        # Wyślij komendę do serwera
        await websocket.send(command)
        print(f"Wysłano komendę '{command}' do serwera.")

# Uruchom funkcję asynchronicznie, podając ścieżkę do obrazu
# file_path = "kamera-zdjecie.jpeg"  # Ścieżka do obrazu, który chcesz wysłać
# asyncio.run(send_image(file_path))


commands = ["forward", "backward", "left", "right", "stop"]

asyncio.run(send_command("run_for:200"))
asyncio.run(send_command("forward"))