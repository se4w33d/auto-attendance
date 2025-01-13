from datetime import datetime
from telegram import Bot


def get_current_day_date() -> str:
    '''
    Returns the current date in the format "Day Date Month Year"
    Eg. "Mon 1 Mar 2022"
    '''
    now = datetime.now()
    return now.strftime("%a %#d %b %Y")


def get_current_day() -> str:
    '''
    Returns the current day
    Eg. "Mon"
    '''
    now = datetime.now()
    return now.strftime("%a")


def generate_heading() -> dict:
    '''
    Generates the heading for the adaptive card
    '''
    if get_current_day() == "Mon":
        heading = f"Online Lecture password ({get_current_day_date()})"
    else:
        heading = f"Lectorial Session password ({get_current_day_date()})"

    return {
        "type": "RichTextBlock",
        "inlines": [
            {
                "type": "TextRun",
                "text": f"{heading}",
                "size": "Medium",
                "weight": "bolder",
            }
        ],
    }


def generate_content(attendance:dict) -> dict:
    '''
    Generates the content for the adaptive card
    '''
    if not attendance:
        return {}
    
    if get_current_day() == "Mon":
        return {
            "type": "RichTextBlock",
            "inlines": [
                {"type": "TextRun", "text": f"{next(iter(attendance.values()))}"}
            ],
        }

    for key, value in attendance.items():
        return {
            "type": "RichTextBlock",
            "inlines": [{"type": "TextRun", "text": f"{key}:    {value}"}],
        }


# Define an async function to send the message
async def send_telegram_message(res_code:str, BOT_TOKEN: str, CHAT_ID: str):
    # Initialize the bot
    bot = Bot(token=BOT_TOKEN)

    if res_code.status_code != 202:
        message = "Failed to send passwords to Teams channel!"
        await bot.send_message(chat_id=CHAT_ID, text=message)
        print("Failed to send notification!")
        return
    
    today = get_current_day_date()
    message = f"{today} passwords sent successfully!"
    await bot.send_message(chat_id=CHAT_ID, text=message)

    print("Notification sent successfully!")
