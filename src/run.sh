google-chrome &
sleep 5
pkill -x "chrome"
sleep 5

# echo "Removing database"
# rm -f ../database.db || { echo "Error deleting DB"; exit 1;}

echo "Running Betano..."
python3 scripts/betano/Betano_Sportrequest.py || { echo "Error running Betano_Sportrequest.py"; exit 1; }

echo "Running Bwin..."
python3 scripts/bwin/Bwin_Sportrequest.py || { echo "Error running Bwin_Sportrequest.py"; exit 1; }

echo "Running CasinoPt..."
python3 scripts/casinopt/CasinoPortugal_Sportrequest.py || { echo "Error running CasinoPortugal_Sportrequest.py"; exit 1; }

echo "Running Lebull..."
python3 scripts/lebull/Lebull_Sportrequest.py || { echo "Error running Lebull_Sportrequest.py"; exit 1; }

echo "Running Processor..."
python3 process_bets/processor.py || { echo "Error running processor.py"; exit 1; }