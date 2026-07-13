from dotenv import load_dotenv
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
import os

load_dotenv()

api_id_value = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")

if not api_id_value or not api_hash:
    raise RuntimeError("Missing API_ID or API_HASH in .env")

try:
    api_id = int(api_id_value)
except ValueError as exc:
    raise RuntimeError("API_ID must be an integer") from exc

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print(client.session.save())