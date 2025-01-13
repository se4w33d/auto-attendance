# Moodle Attendance Password Fetcher
This project automates the process of fetching attendance passwords from the Moodle platform and sending them to a Microsoft Teams channel for students. Subsequently, sending notification to a Telegram bot informing whether the task is successful or not.

## Requirement
Create a .env file in the root directory and add the following environment variables:
```
USER = your_username
PASSWORD = your_password
MOODLE_URL = your_moodle_url
TEAM_WEBHOOK_URL = your_teams_webhook_url
TEAM_WEBHOOK_URL_FOR_TESTING = your_teams_webhook_url_for_testing
TELEGRAM_BOT_TOKEN = your_telegram_bot_token
TELEGRAM_CHAT_ID = your_telegram_chat_id
```

## Usage
1. Run the script:
```python
python src/main.py
```

2. The script will:
   * Log in to the Moodle platform.
   * Fetch the attendance passwords for the current day.
   * Send the passwords to the specified Microsoft Teams channel.
   * Send a notification to the specified Telegram bot.


## Project Files
`main.py`: The main script that orchestrates the entire process.  
`play.py`: Contains functions to interact with the Moodle platform using Playwright.  
`utility.py`: Contains utility functions for date formatting and sending Telegram messages.  