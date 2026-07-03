import re
import os
from dotenv import load_dotenv
from telethon import TelegramClient, events

# ===========================
# YOUR INFO
# ===========================

load_dotenv()

api_id = os.getenv("API_ID")
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

client = TelegramClient("session", api_id, api_hash)


def looks_like_job(text):

    if text is None:
        return False

    required = [
        "Job Title:",
        "Job Type:",
        "Work Location:"
    ]

    return all(x in text for x in required)


def get_job_title(text):

    m = re.search(r"Job Title:\s*(.+)", text)

    if m:
        return m.group(1).strip().lower()

    return ""


def get_job_type(text):

    m = re.search(r"Job Type:\s*(.+)", text)

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


@client.on(events.NewMessage(chats=CHANNEL))
async def handler(event):

    text = event.raw_text

    # Ignore ads/promotions
    if not looks_like_job(text):
        return

    title = get_job_title(text)
    job_type = get_job_type(text)

    if blocked(title):
        return

    if not wanted(job_type):
        return

    print(f"Matched -> {title}")

    # Forward to Saved Messages
    await event.forward_to("me")


print("Running...")
client.start()
client.run_until_disconnected()