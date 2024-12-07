import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ShadowsocksClient:
    def __init__(self, server_host='127.0.0.1', server_port=8388):
        self.server_host = server_host
        self.server_port = server_port
    
    async def connect(self):
        try:
            reader, writer = await asyncio.open_connection(
                self.server_host,
                self.server_port
            )
            
            logger.info(f'Connected to server {self.server_host}:{self.server_port}')
            
            # Send test data
            message = b'Hello, Shadowsocks!'
            writer.write(message)
            await writer.drain()
            
            # Receive response
            data = await reader.read(8192)
            logger.info(f'Received: {data.decode()}')
            
            writer.close()
            await writer.wait_closed()
            
        except Exception as e:
            logger.error(f'Connection error: {e}')

# Run the client
if __name__ == '__main__':
    client = ShadowsocksClient()
    asyncio.run(client.connect())