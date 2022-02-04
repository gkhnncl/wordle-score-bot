# wordle-score-bot
Telegram bot for tracking scores in group chats playing Wordle

## Google Sheets integration

1. Install `gspread`.
2. Create an OAuth client for authentication and save it as `credentials.json` in the folder. See [this](https://docs.gspread.org/en/latest/oauth2.html#for-end-users-using-oauth-client-id) for more information.
3. Create your Google Sheet and add `SHEET_URL=https://docs.google.com/spreadsheets/d/...'` to the `.env` file.
