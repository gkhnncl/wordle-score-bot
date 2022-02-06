# wordle-score-bot
Telegram bot for tracking scores in group chats playing Wordle

![demo](https://user-images.githubusercontent.com/13794421/152672850-daf0866d-312b-4f78-8238-68e9241a0ded.gif)

Add the bot to your Wordle group chat to log everyone's scores in a local CSV file or Google Sheets.

## Usage guide

1. Clone this repo and install `requirements.txt`.
2. Create your bot via the [BotFather](https://core.telegram.org/bots#6-botfather).
3. Set privacy settings to allow reading messages from group chats. (Detailed screenshots to be added soon.)
4. Set the `TOKEN` variable to your bot's access token in the `.env` file.
5. Run `python bot.py`.

## Google Sheets integration (optional)

1. Install `gspread`.
2. Create an OAuth client for authentication and save it as `credentials.json` in the folder. See [this](https://docs.gspread.org/en/latest/oauth2.html#for-end-users-using-oauth-client-id) for more information.
3. Create your Google Sheet and add `SHEET_URL=https://docs.google.com/spreadsheets/d/...'` to the `.env` file.

## TODO list

- [ ] Score validation for repeated posts
- [ ] Daily summary messages
- [ ] Weekly/monthly leaderboard

