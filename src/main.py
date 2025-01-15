import requests
import json
import asyncio
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv, dotenv_values
from utility import generate_heading, generate_content, send_telegram_message
from play import run

# Load environment variables from .env
load_dotenv()

LOGIN = {
    "url": dotenv_values(".env")["MOODLE_URL"],
    "user": dotenv_values(".env")["USER"],
    "password": dotenv_values(".env")["PASSWORD"]
}

day = {
    "Mon": "cs385s25-a.sg",
    "Tue": ["cs385s25-b.sg", "csd3185s25-a.sg", "csd3186s25-a.sg", "csd3186s25-b.sg"],
    "Thu": ["cs385s25-a.sg", "csd3185s25-b.sg", "csd3186s25-c.sg", "csd3186s25-d.sg"]
}

teams_url = dotenv_values(".env")["TEAM_WEBHOOK_URL"]
teams_url_test = dotenv_values(".env")["TEAM_WEBHOOK_URL_FOR_TESTING"]

attendance = {}


# Run the show capturing the attendance passwords
with sync_playwright() as playwright:
    run(playwright, LOGIN, attendance, day)

print(attendance)


# Send the attendance passwords to the teams channel
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

adaptive_card = {
    "type": "message",
    "attachments": [
        {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "contentUrl": None,
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.2",
                "body": None,
            },
        }
    ],
}

body_elements = []

heading = generate_heading()
content = generate_content(attendance)
if not content:
    print("Attendance passwords is empty!")
    exit()

body_elements.append(heading)
body_elements.extend(content)

adaptive_card["attachments"][0]["content"]["body"] = body_elements

adaptive_card = json.dumps(adaptive_card)

response = requests.post(teams_url_test, headers=headers, data=adaptive_card)


# Send notifications to telegram
BOT_TOKEN = dotenv_values(".env")["TELEGRAM_BOT_TOKEN"]
CHAT_ID = dotenv_values(".env")["TELEGRAM_CHAT_ID"]

asyncio.run(send_telegram_message(response, BOT_TOKEN, CHAT_ID))
