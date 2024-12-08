import asyncio
import logging
import json
import os
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ShadowsocksServer:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.host = self.config['server']
        self.port = self.config['server_port']
        self.password = self.config['password']
        self.method = self.config['method']
        self.timeout = 300
        
    def load_config(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(config_path, 'r') as f:
            return json.load(f)
            
    async def handle_connection(self, reader, writer):
        addr = writer.get_extra_info('peername')
        logger.info(f'New connection from {addr}')
        
        try:
            while True:
                data = await reader.read(8192)
                if not data:
                    break
                    
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
        logger.info(f'Encryption method: {self.method}')
        
        async with server:
            await server.serve_forever()

def parse_args():
    parser = argparse.ArgumentParser(description='Shadowsocks server')
    parser.add_argument('-c', '--config', required=True, help='Path to config file')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    server = ShadowsocksServer(args.config)
    asyncio.run(server.start())