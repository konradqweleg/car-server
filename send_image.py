import asyncio
import websockets

async def send_image(file_path: str):
    # Adres serwera WebSocket
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        # Wczytaj obraz JPEG jako dane binarne i wyślij do serwera
        with open(file_path, "rb") as image_file:
            image_data = image_file.read()
            await websocket.send(image_data)
            print(f"Wysłano obraz '{file_path}' do serwera.")



# Uruchom funkcję asynchronicznie, podając ścieżkę do obrazu
file_path = "image.jpg"  # Ścieżka do obrazu, który chcesz wysłać
asyncio.run(send_image(file_path))
