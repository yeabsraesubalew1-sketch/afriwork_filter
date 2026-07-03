import re
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ===========================
# YOUR INFO
# ===========================

load_dotenv()

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

CHANNEL = "freelance_ethio"

# ===========================
# FILTERS
# ===========================

# Job types we want
GOOD_TYPES = [
    "remote",
    "part-time",
    "contractual",
    "hybrid"
]

# Jobs to ignore
BLOCKED_KEYWORDS = [

    # Accounting
    "accountant",
    "accounting",
    "bookkeeper",
    "finance",

    # Graphic design
    "graphic designer",
    "graphics designer",
    "graphic design",
    "illustrator",

    # Video
    "video editor",
    "video editing",
    "videographer",

    # Social media
    "social media",
    "content creator",
    "content manager",
    "host",
    "tiktok",
    "instagram",
    "youtube",

]

client = TelegramClient(StringSession(os.getenv("SESSION")), api_id, api_hash)


def normalize_text(text):
    if not text:
        return ""

    return re.sub(r"\s+", " ", text).strip().lower()


def looks_like_job(text):
    if not text:
        return False

    normalized = normalize_text(text)

    return all(marker in normalized for marker in ["job title", "job type", "work location"])


def get_job_title(text):
    m = re.search(r"job title\s*[:\-]\s*(.+)", text, re.I)

    if m:
        return m.group(1).strip().lower()

    return ""


def get_job_type(text):
    m = re.search(r"job type\s*[:\-]\s*(.+)", text, re.I)

    if m:
        return m.group(1).strip().lower()

    return ""


def blocked(title):

    for word in BLOCKED_KEYWORDS:
        if word in title:
            return True

    return False


def wanted(job_type):

    for t in GOOD_TYPES:
        if t in job_type:
            return True

    return False


@client.on(events.NewMessage(chats=CHANNEL, incoming=True))
async def handler(event):
    text = event.raw_text or event.message.message or ""

    if not looks_like_job(text):
        return

    title = get_job_title(text)
    job_type = get_job_type(text)

    if not title or not job_type:
        return

    if blocked(title):
        return

    if not wanted(job_type):
        return

    print(f"Matched -> {title} ({job_type})")

    try:
        me = await client.get_me()
        await client.forward_messages(me, event.message)
        print("Forwarded to Saved Messages")
    except Exception as exc:
        print(f"Forward failed: {exc}")
        try:
            await client.send_message("me", text)
        except Exception as fallback_exc:
            print(f"Fallback send failed: {fallback_exc}")


print("Running... waiting for new messages")
client.start()
client.run_until_disconnected()