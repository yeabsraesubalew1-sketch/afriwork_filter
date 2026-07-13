# Afriwork Filter

Afriwork Filter is a small Telegram monitor that watches the `freelance_ethio` channel, looks for job posts that match a simple title/type filter, forwards matching posts to Saved Messages, and raises a desktop or sound alert when a match is found.

## What it does

- Connects to Telegram with a `StringSession`.
- Watches incoming messages from the `freelance_ethio` channel.
- Detects posts that look like job listings by checking for `Job Title`, `Job Type`, and `Work Location` fields.
- Keeps only jobs whose type contains one of these values: `remote`, `part-time`, `contractual`, or `hybrid`.
- Skips jobs whose title contains blocked keywords such as accounting, graphic design, video editing, or social media roles.
- Forwards matching posts to your Saved Messages and triggers a notification.
- Exposes a lightweight health endpoint on `/` and `/health` for deployment platforms such as Fly.io.

## Requirements

- Python 3.10 or newer
- A Telegram API ID and API hash from https://my.telegram.org
- A valid Telegram StringSession for the account that should run the filter

## Setup

1. Create and activate a virtual environment.

	```bash
	python -m venv .venv
	.venv\Scripts\activate
	```

2. Install dependencies.

	```bash
	pip install -r requirements.txt
	```

3. Create a `.env` file in the project root.

	```env
	API_ID=123456
	API_HASH=your_api_hash
	SESSION=your_telethon_string_session
	PORT=8080
	DISABLE_NOTIFICATIONS=0
	```

## Generating a StringSession

Use `sessionstring.py` to generate a new session string for the Telegram account you want the bot to use. The script reads `API_ID` and `API_HASH` from the same `.env` file used by the bot.

1. Make sure your `.env` file contains `API_ID` and `API_HASH`.
2. Run the script.

	```bash
	python sessionstring.py
	```

3. Copy the printed session string into `SESSION` in your `.env` file.

## Running Locally

Start the bot with:

```bash
python bot.py
```

When the required environment variables are present, the bot connects to Telegram, starts the health server, and begins watching the channel immediately.

## Deployment Notes

- The app listens on the `PORT` environment variable and responds to `GET /` and `GET /health` with `ok`.
- The included `Dockerfile` and `fly.toml` are set up for container deployment.
- On Fly.io, store `API_ID`, `API_HASH`, and `SESSION` as secrets before deploying.

## Configuration

The filtering logic lives in `bot.py`.

- Update `CHANNEL` if you want to watch a different Telegram channel.
- Adjust `GOOD_TYPES` to change which job types are accepted.
- Edit `BLOCKED_KEYWORDS` to add or remove job categories you want to ignore.

## Troubleshooting

- If the bot prints that Telegram environment variables are missing, check your `.env` file and ensure `API_ID`, `API_HASH`, and `SESSION` are set.
- If Telegram rejects the session, generate a fresh `StringSession` and try again.
- If desktop notifications fail, set `DISABLE_NOTIFICATIONS=1` to keep the bot running without alerts.

