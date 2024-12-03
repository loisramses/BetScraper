import json
import os
import re
from rich import print
from collections import defaultdict
from utils.maps import *

# def load_data(file_paths):
#     consolidated_data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(list))))
    
#     for file_path in file_paths:
#         with open(file_path, 'r') as f:
#             data = json.load(f)
#             for sport, leagues in data.items():
#                 for league, matches in leagues.items():
#                     for match in matches:
#                         for match_name, match_data in match.items():
#                             for bet_type, bets in match_data['bets']:
#                                 consolidated_data[sport][league][match_name][bet_type].extend(bets)
    
#     return consolidated_data

def load_data(file_paths):
    resulting_data = []
    
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for _, leagues in data.items():
                for _, matches in leagues.items():
                    for match in matches:
                        for _, match_data in match.items():
                            for bet_type, bet_selections in match_data['bets']:
                                if bet_type in bet_type_mapping:
                                    for selection in bet_selections:
                                        selection[0] = selection[0].replace(',', '.')
                                        if re.search('mais', selection[0], re.IGNORECASE):
                                            selection[0] = selection_normalization['more'] + re.search(pattern, selection[0])[0]
                                        elif re.search('menos', selection[0], re.IGNORECASE):
                                            selection[0] = selection_normalization['less'] + re.search(pattern, selection[0])[0]
                                    resulting_data.append(bet_selections)
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
