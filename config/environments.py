import json

from dotenv import load_dotenv
from os import getenv

load_dotenv()

DISCORD_TOKEN = getenv('DISCORD_TOKEN')
MANAGER_ROLE = getenv('MANAGER_ROLE')
DATABASE_URL = getenv('DATABASE_URL')
CF_RESOLVER_URL = getenv('CF_RESOLVER_URL')
PROXY_IP = getenv('PROXY_IP')

with open('config/config.json', 'rb') as f:
    DATA_CONFIG = json.load(f)
