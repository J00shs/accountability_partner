# Accountability Bot

In front of you is the code to a Discord bot I built using Python. 

## Features
Currently, the bot keeps track of how long a user studies. Once they've completed a session, it gets added into a channel for the extra accountability.

More features are planned.

## Getting Started
### 1. Clone the Repo
```bash
git clone https://github.com/J00shs/accountability_partner
cd accountability_partner
```
### 2. Set up the '.env'
```bash
DISCORD_TOKEN=your_token
DB_NAME=name_for_your_created_database
CHANNEL_NAME=channel_for_bot_to_watch
CHANNEL_ID=id_of_error_reporting_channel
DIZZY=your_discord_user_name_for_@_mentions
LOG_ACTIVITY=id_of_channel_for_session_record
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```
### 4. Run the bot

```bash
python3 channel_tracker.py
```


