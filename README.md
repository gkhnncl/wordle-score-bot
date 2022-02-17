# wordle-score-bot
Telegram bot for tracking scores in group chats playing Wordle

![demo](https://user-images.githubusercontent.com/13794421/152672850-daf0866d-312b-4f78-8238-68e9241a0ded.gif)

Add the bot to your Wordle group chat to log everyone's scores in a local CSV file or Google Sheets.

## Features and commands

- `/recap` - Get the leaderboards of the last two Wordle editions.
- `/weekly` - Get the leaderboard of the past week (starting from yesterday).
- Google Sheets integration (optional)
- TODO: Monthly leaderboards

## Usage guide

1. Clone this repo and install `requirements.txt`.

    ``` sh
    $ git clone git@github.com:ajdajd/wordle-score-bot.git
    $ cd wordle-score-bot
    $ pip install -r requirements.txt
    ```

2. Create your bot via the [BotFather](https://core.telegram.org/bots#6-botfather).

    ![image](https://user-images.githubusercontent.com/13794421/152684527-775f284f-923f-4555-93d9-4cbc1a617fec.png)
    
3. Turn off group privacy to allow reading messages from group chats.

   1. Enter `/mybots` and select your bot.
   2. Go to `Bot Settings` > `Group Privacy`. Select `Turn off`.

   ![image](https://user-images.githubusercontent.com/13794421/152685053-5a14ccf5-1320-470c-b8a3-354d21732854.png)

4. Set the `TOKEN` variable to your bot's access token in the `.env` file.
5. Run `bot.py`.

    ``` sh
    $ python bot.py
    ```

    or 

    ``` sh
    $ nohup python -u /home/ubuntu/wordle-score-bot/bot.py &
    ```
    
    to keep it running in the background.

Messages received containing `Wordle XXX Y/6` will be logged into `scores.csv`. It will be created automatically if not yet existing.

## Google Sheets integration (optional)

1. Install `gspread`.
2. Create a service account for authentication and save it as `service_account.json` in the root folder. See [this](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account) for more information.
3. Create your Google Sheet and share it with the `client_email` of the service account.
4. Add `SHEET_URL=https://docs.google.com/spreadsheets/d/...'` to the `.env` file.

## Weekly leaderboard scheduled message (optional)

1. Obtain the chat ID of your group. See [this SO thread](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id) for more information.
2. Add `CHAT_ID=-XXXXXXXXX` to the `.env` file.
3. Edit `constants.py` to change time and day of message. The default setting is every Friday at 04:00 (UTC).
