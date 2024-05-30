from dotenv import load_dotenv
from os import getenv

load_dotenv()

DISCORD_TOKEN = getenv('DISCORD_TOKEN')
MANAGER_ROLE = getenv('MANAGER_ROLE')
DATABASE_URL = getenv('DATABASE_URL')
