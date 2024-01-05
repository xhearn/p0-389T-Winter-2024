import requests
import time
import json
import os
import random
from dotenv import load_dotenv

load_dotenv()

BOT_ID = os.getenv("BOT_ID")
GROUP_ID = os.getenv("GROUP_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
LAST_MESSAGE_ID = None
MY_SENDER_ID = os.getenv("MY_SENDER_ID")
TWINWORD_API_KEY = os.getenv("TWINWORD_API_KEY")
TWINWORD_API_HOST = os.getenv("TWINWORD_API_HOST")

def analyze_sentiment(text):
    url = "https://twinword-twinword-bundle-v1.p.rapidapi.com/sentiment_analyze/"
    headers = {
        "X-RapidAPI-Key": TWINWORD_API_KEY,
        "X-RapidAPI-Host": TWINWORD_API_HOST
    }
    params = {"text": text}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def categorize_sentiment(score):
    responses = {
        "very very negative": ["That's not a nice thing to say.", "That's quite harsh."],
        "very negative": ["That's a bit negative.", "Try to be a bit more positive."],
        "negative": ["That's slightly negative.", "Could be more positive."],
        "neutral": ["Why yes that makes sense", "I see your point."],
        "positive": ["That's fairly positive.", "That's a good vibe!"],
        "very positive": ["That's very positive!", "Great to hear!"],
        "very very positive": ["That's excellent to hear!", "Such positivity!"],
    }
    if score <= -0.75:
        return random.choice(responses["very very negative"])
    elif -0.75 < score <= -0.5:
        return random.choice(responses["very negative"])
    elif -0.5 < score < 0.0:
        return random.choice(responses["negative"])
    elif 0.0 <= score <= 0.25:
        return random.choice(responses["neutral"])
    elif 0.25 < score <= 0.5:
        return random.choice(responses["positive"])
    elif 0.5 < score <= 0.75:
        return random.choice(responses["very positive"])
    else:  # score > 0.75
        return random.choice(responses["very very positive"])

def send_message(text, attachments=None):
    """Send a message to the group using the bot."""
    post_url = "https://api.groupme.com/v3/bots/post"
    data = {"bot_id": BOT_ID, "text": text, "attachments": attachments or []}
    response = requests.post(post_url, json=data)
    return response.status_code == 202


def get_group_messages(since_id=None):
    """Retrieve recent messages from the group."""
    params = {"token": ACCESS_TOKEN}
    if since_id:
        params["since_id"] = since_id

    get_url = f"https://api.groupme.com/v3/groups/{GROUP_ID}/messages"
    response = requests.get(get_url, params=params)
    if response.status_code == 200:
        # this shows how to use the .get() method to get specifically the messages but there is more you can do (hint: sample.json)
        return response.json().get("response", {}).get("messages", [])
    return []


def process_message(message):
    """Process and respond to a message."""
    global LAST_MESSAGE_ID
    text = message["text"].lower()
    sender_id = message["sender_id"] #Get the senders ID
    sender_name = message["name"] #Get the senders name
    sender_type = message["sender_type"]

    # i.e. responding to a specific message (note that this checks if "hello bot" is anywhere in the message, not just the beginning)
    if sender_type == "bot":
        pass #Do nothing
    elif "good morning" in text:
        send_message("Good morning, " + sender_name + "!")
    elif "good night" in text:
        send_message("Good night, " + sender_name + "!")
    elif sender_id == MY_SENDER_ID:
        sentiment_result = analyze_sentiment(text)
        if sentiment_result and 'score' in sentiment_result:
            sentiment_response = categorize_sentiment(sentiment_result['score'])
            send_message(f"{sender_name}, {sentiment_response}")
    LAST_MESSAGE_ID = message["id"]


def main():
    global LAST_MESSAGE_ID
    # Fetch the latest messages to set the initial LAST_MESSAGE_ID
    recent_messages = get_group_messages()
    if recent_messages:
        LAST_MESSAGE_ID = recent_messages[0]["id"]  # Set to the latest message ID

    while True:
        messages = get_group_messages(LAST_MESSAGE_ID)
        if messages:
            # Update LAST_MESSAGE_ID to the latest message in this batch
            LAST_MESSAGE_ID = messages[0]["id"]
        for message in reversed(messages):
            process_message(message)
        time.sleep(10)


if __name__ == "__main__":
    main()
