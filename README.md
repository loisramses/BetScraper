# Betting Odds Scraper & Advantage Betting Notifier

## Overview

This project is a web scraping system that collects odds from four Portuguese betting websites, compares them, and identifies advantage betting opportunities. The detected opportunities are then sent to a Telegram channel, where users receive real-time notifications.

## Features

- Scrapes odds from four betting websites

- Compares odds to detect value betting opportunities

- Automated notifications sent to a Telegram channel

- Optimized data processing for efficiency and reliability

## Technologies Used

- **Python** (Core development)

- **Nodriver** (Scraping)

- **Telegram API** (Notification system)

- **SQLite** (Data storage)

- **AsyncIO** (Asynchronous requests for efficiency)

## Installation & Setup

### Clone this repository:
```bash
    git clone https://github.com/loisramses/BetScraper.git
    cd BetScraper
```

### Install dependencies:
```bash
    python -m venv venv
    source venv/bin/activate
    pip install zendriver requests rapidfuzz
    mkdir src/logs
    mkdir src/ouput
```

### Configure environment variables for Telegram bot:
```bash
    export TELEGRAM_BOT_TOKEN="your_token_here"
    export TELEGRAM_CHAT_ID="your_chat_id_here"
```

### Run the scraper:
```bash
    bash start.sh
```

## Usage

### To run periodically, create a crontab:
```bash
    crontab -e
```

### And then, at the end of the file:
```bash
    */<minute_interval> * * * * /path/to/your/folder/BetScraper.sh
```

If an advantage betting opportunity is found, it is sent to the configured Telegram channel.

## Future Improvements

Expand to more betting websites.

## License

This project is for personal and educational purposes. Use at your own discretion.
