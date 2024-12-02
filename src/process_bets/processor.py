import json
import os
from rich import print
from collections import defaultdict

def load_data(file_paths):
    consolidated_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for sport, leagues in data.items():
                for league, matches in leagues.items():
                    for match in matches:
                        for match_name, match_data in match.items():
                            for bet_type, bets in match_data['bets']:
                                consolidated_data[sport][league][match_name][bet_type].extend(bets)
    
    return consolidated_data

folder_path = 'src/output/'
file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)]

all_data = load_data(file_paths)

with open('./src/process_bets/data.json', 'w', encoding='utf-8') as file:
    json.dump(all_data, file, ensure_ascii=False, indent=2)
