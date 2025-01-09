chromium --headless &
sleep 10
pkill -x "chromium"
sleep 5

echo "Running Scraper..."
python3 scripts/scraper.py || { echo "Error running scraper.py"; exit 1; }

echo "Running Processor..."
python3 process_bets/processor.py || { echo "Error running processor.py"; exit 1; }