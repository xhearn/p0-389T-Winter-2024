# GroupMe Bot

## Features

- Responds to "good morning" and "good night" with a personalized greeting.
- Analyzes sentiment of each message and responds with customized feedback based on the sentiment score:
  - Very Very Negative to Very Very Positive responses.
- Ignores messages from other bots to prevent loops.

## How to Run the Bot

1. Ensure Python 3 and `pip` are installed on your system.
2. Install the required packages by running `pip install requests python-dotenv`.
3. Set up your `.env` file with the following variables:
   - `BOT_ID`: Your GroupMe Bot ID.
   - `GROUP_ID`: The GroupMe Group ID where the bot will operate.
   - `ACCESS_TOKEN`: Your GroupMe Developer access token.
   - `MY_SENDER_ID`: Your personal GroupMe user ID.
   - `TWINWORD_API_KEY`: Your Twinword Sentiment Analysis API key.
   - `TWINWORD_API_HOST`: The host for the Twinword API.
4. Run the bot with the command `python bot.py` from within the `groupme-bot` directory.

Make sure to replace the placeholder values with your actual credentials and IDs.
