import json
import os
import re
from rich import print
from collections import defaultdict
from utils.maps import bet_type_mapping
from utils.standards import selection_standardization

def load_data(file_paths):
    resulting_data = []
    
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for sport_name, leagues in data.items():
                for league_name, matches in leagues.items():
                    for match in matches:
                        for match_name, match_data in match.items():
                            for bet_type, bet_selections in match_data['bets']:
                                if bet_type in bet_type_mapping:
                                    print(bet_type_mapping[bet_type].value)
                                    for selection in bet_selections:
                                        selection[0] = selection[0].replace(',', '.')
                                        if re.search('mais', selection[0], re.IGNORECASE):
                                            selection[0] = selection_standardization['more'] + re.search(pattern, selection[0])[0]
                                        elif re.search('menos', selection[0], re.IGNORECASE):
                                            selection[0] = selection_standardization['less'] + re.search(pattern, selection[0])[0]
                                    resulting_data.append(match_data)
    return resulting_data

folder_path = 'src/output'
file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)]
pattern = re.compile('([0-9]*[.])?[0-9]+')
all_data = load_data(file_paths) 
# all_data = load_data(file_paths[:1]) 
# all_data = load_data(file_paths[1:2])
# all_data = load_data(file_paths[2:3])
# all_data = load_data(file_paths[3:4])
# all_data = "\n".join(name for name in all_data)

with open('./src/process_bets/data.json', 'w', encoding='utf-8') as file:
    json.dump(all_data, file, ensure_ascii=False, indent=2)
    
# with open('./src/process_bets/data.json', 'w', encoding='utf-8') as file:
#     file.write(all_data)
