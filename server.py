from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import asyncio

from test_socket_client import test_client
from socket_server import SocketServer

START_TESTING_SOCKET_CLIENT = True

socket_server = SocketServer()
app = FastAPI()
templates = Jinja2Templates(directory="templates")


async def websocket_reader(websocket, queue):
    """ Puts messages from websocket to queue """
    # Needs try block to block WebSocketDisconnect exception 
    try:
        while True:
            data = await websocket.receive_text()
            print('WS <', data)
            await queue.put(data + '\n')
    except WebSocketDisconnect:
        print('Stopping WS Reader (received WebSocketDisconnect)')


async def websocket_writer(websocket, queue):
    """ Puts messages from queue to websocket """
    # Needs try block to block WebSocketDisconnect exception 
    try:
        while True:
            data = await queue.get()
            print('WS >', data)
            await websocket.send_text(data)
    except WebSocketDisconnect:
        print('Stopping WS Writer (received WebSocketDisconnect)')


@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Creating a queue for messages that will be sent to websocket
    # And adding this queue to SocketServer's outbound_queues
    websocket_queue = asyncio.Queue()
    socket_server.outbound_queues.append(websocket_queue)
    # Starting reader in background...
    asyncio.create_task(websocket_reader(websocket, socket_server.inbound_queue))
    # ... and awaiting writer because we do not want this function to
    # finish while connection is open
    try:
        await websocket_writer(websocket, websocket_queue)
    finally:
        socket_server.outbound_queues.remove(websocket_queue)
        print('Websocket disconnected')


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("root.html", context={'request': request})


@app.on_event("startup")
async def startup_event():
    await socket_server.start_server()
    if START_TESTING_SOCKET_CLIENT:
        asyncio.create_task(test_client())


@app.on_event("shutdown")
async def shutdown_event():
    await socket_server.shut_down()
