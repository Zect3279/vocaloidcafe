import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ['TOKEN']
REDIS_URL = os.environ['REDIS_URL']