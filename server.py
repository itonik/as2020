""" 
Main server part

1. Template server
2. Websocket server
3. Socket server
"""

from fastapi import FastAPI, WebSocket
import asyncio


app = FastAPI()
inbound_queue = asyncio.Queue()
outbound_queue = asyncio.Queue()


async def ws_to_queue(websocket: WebSocket):
    while True:
        data = await websocket.receive_text()
        print(f'WS -> Q: {data}')
        await inbound_queue.put(data)


async def queue_to_ws(websocket: WebSocket):
    while True:
        data = await outbound_queue.get()
        print(f'Q -> WS: {data}')
        await websocket.send(data)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    asyncio.create_task(ws_to_queue(websocket))
    asyncio.create_task(queue_to_ws(websocket))


@app.get("/")
async def root():
    # asyncio.create_task(background_print())
    return {"message": "Hello World"}


@app.on_event("startup")
async def startup_event():
    pass