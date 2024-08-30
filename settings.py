import os
from dotenv import load_dotenv

load_dotenv()

EXPIRED_TIME = 900
JWT_SECRET = os.getenv("JWT_SECRET")