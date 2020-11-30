import asyncio

class SocketServer:
    def __init__(self, port=8001):
        """
        One client socket server

        Sends message from inbound_queue to socket and
        from socket to outbound_queues
        """
        self.reader: asyncio.StreamReader = None
        self.writer: asyncio.StreamWriter = None
        self.inbound_queue = asyncio.Queue()
        self.outbound_queues: list[asyncio.Queue] = []
        
        self.server: asyncio.Server = None
        self.port = port

    async def start_server(self):
        self.server = await asyncio.start_server(
            self.new_connecion_callback,
            port=self.port
        )
        asyncio.create_task(self.server.serve_forever())

    async def new_connecion_callback(self, reader, writer):
        """
        Callback that is passed to asyncio.start_server
        """
        if self.reader:
            await self.close_connection(
                'Allready connected. Closing...',
                writer
            )
            return
        self.reader = reader
        self.writer = writer
        asyncio.create_task(self.reader_worker())
        asyncio.create_task(self.writer_worker())

    async def close_connection(self, mesage: str, writer: asyncio.StreamWriter):
        """
        Writes goodbye message and closes connection
        """
        writer.write('Already connected. Closing...')
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def reader_worker(self):
        """
        Passes data from reader to outbound_queues
        """
        try:
            while True:
                data = await self.reader.readline()
                print('SOCKET <', data)
                for queue in self.outbound_queues:
                    await queue.put(data.decode())
        finally:
            self.reader = None    

    async def writer_worker(self):
        """
        Passes data from inbound_queue to writer
        """
        try:
            while True:
                data = await self.inbound_queue.get()
                print('SOCKET > ', data)
                self.writer.write(data.encode())
                await self.writer.drain()
        finally:
            self.writer = None

    async def shut_down(self):
        self.server.close()
        await self.server.wait_closed()
