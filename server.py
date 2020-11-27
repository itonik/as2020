""" 
Main server part

1. Template server
2. Websocket server
3. Socket server
"""

from fastapi import FastAPI
import asyncio

app = FastAPI()


async def background_print():
    for i in range(10):
        print(f'Yo {i}')
        await asyncio.sleep(1)


@app.get("/")
async def root():
    asyncio.create_task(background_print())
    return {"message": "Hello World"}
