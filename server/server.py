import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ShadowsocksServer:
    def __init__(self, host='0.0.0.0', port=8388):
        self.host = host
        self.port = port
        
    async def handle_connection(self, reader, writer):
        addr = writer.get_extra_info('peername')
        logger.info(f'New connection from {addr}')
        
        try:
            while True:
                data = await reader.read(8192)
                if not data:
                    break
                    
                # Echo the received data back (for testing)
                writer.write(data)
                await writer.drain()
                
        except Exception as e:
            logger.error(f'Error handling connection: {e}')
        finally:
            writer.close()
            await writer.wait_closed()
            logger.info(f'Connection closed from {addr}')
    
    async def start(self):
        server = await asyncio.start_server(
            self.handle_connection,
            self.host,
            self.port
        )
        
        logger.info(f'Server started on {self.host}:{self.port}')
        
        async with server:
            await server.serve_forever()

# Run the server
if __name__ == '__main__':
    server = ShadowsocksServer()
    asyncio.run(server.start())