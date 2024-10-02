# Discord XP Bot for Role Assignment and Announcements

## Overview

This bot is designed to help manage and reward user activity on a Discord server by tracking XP for users based on message activity and referrals. As users earn XP, they will be assigned roles at certain thresholds. Additionally, the bot allows for sending announcements to specific channels, including support for image attachments.

## Features

- **XP System:** Users earn XP from regular messages and referrals.
- **Role Assignment:** Automatic role assignment based on XP milestones.
- **Announcements:** Send messages to specific channels with optional image attachments.
- **User Data Persistence:** User data is saved in a JSON file for persistence across bot sessions.

## Installation

### Prerequisites

- Python 3.6+
- `discord.py` library
- `aiohttp` library

### Steps

1. Clone this repository.
2. Install the required Python packages:

    ```bash
    pip install discord.py aiohttp
    ```

3. Set up your Discord bot token as an environment variable:

    ```bash
    export DISCORD_BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
    ```

4. Run the bot:

    ```bash
    python bot.py
    ```

## Commands

- `!xp`: Displays your current XP.
- `!announce <channel_name> <message>`: Sends a message to a specific channel. You can attach an image by uploading it with the command.

## XP Thresholds and Roles

- **100 XP:** Pluse
- **200 XP:** Riff
- **400 XP:** Rhythm
- **800 XP:** Harmony
- **1600 XP:** Tempo

The bot will automatically assign the appropriate role to users based on their XP.

## License

This project is licensed under the MIT License.
