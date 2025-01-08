echo "Running Scraper..."
python3 src/scripts/scraper.py || { echo "Error running scraper.py"; exit 1; }

echo "Running Processor..."
python3 src/process_bets/processor.py || { echo "Error running processor.py"; exit 1; }