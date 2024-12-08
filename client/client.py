import asyncio
import logging
import json
import os
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ShadowsocksClient:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.server_host = self.config['server']
        self.server_port = self.config['server_port']
        self.local_address = self.config['local_address']
        self.local_port = self.config['local_port']
        self.password = self.config['password']
        self.method = self.config['method']
        self.timeout = 300
        
    def load_config(self, config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        with open(config_path, 'r') as f:
            return json.load(f)
    
    async def connect(self):
        try:
            reader, writer = await asyncio.open_connection(
                self.server_host,
                self.server_port
            )
            
            logger.info(f'Connected to server {self.server_host}:{self.server_port}')
            
            message = b'Hello, Shadowsocks!'
            writer.write(message)
            await writer.drain()
            
            data = await reader.read(8192)
            logger.info(f'Received: {data.decode()}')
            
            writer.close()
            await writer.wait_closed()
            
        except Exception as e:
            logger.error(f'Connection error: {e}')

def parse_args():
    parser = argparse.ArgumentParser(description='Shadowsocks client')
    parser.add_argument('-c', '--config', required=True, help='Path to config file')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    client = ShadowsocksClient(args.config)
    asyncio.run(client.connect())