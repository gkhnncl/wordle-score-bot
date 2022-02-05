# wordle-score-bot
Telegram bot for tracking scores in group chats playing Wordle

## Installation

1. Create your bot via the [BotFather](https://core.telegram.org/bots#6-botfather).
2. Set privacy settings to allow reading messages from group chats. (Detailed screenshots to be added soon.)
2. Clone this repo.
3. Install `requirements.txt`.
4. Run `python bot.py`.

## Google Sheets integration (optional)

1. Install `gspread`.
2. Create an OAuth client for authentication and save it as `credentials.json` in the folder. See [this](https://docs.gspread.org/en/latest/oauth2.html#for-end-users-using-oauth-client-id) for more information.
3. Create your Google Sheet and add `SHEET_URL=https://docs.google.com/spreadsheets/d/...'` to the `.env` file.

## TODO list

- [ ] Score validation for repeated posts
- [ ] Daily summary messages
- [ ] Weekly/monthly leaderboard
