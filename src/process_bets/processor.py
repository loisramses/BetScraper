import json
import os
import re
from rich import print
from utils.maps import *
from utils.standards import *
from utils.db_manager import *
from utils.my_types import *

def insert_data(file_paths):
    conn = get_connection('database.db')
    cursor = conn.cursor()
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for sport_name, leagues in data.items():
                sport_id = get_sport(cursor, sport_name)
                if not sport_id:
                    continue
                for league_name, matches in leagues.items():
                    league_id = insert_league(cursor, league_name, sport_id)
                    for match in matches:
                        for match_name, match_data in match.items():
                            parts = match_name.split(":")
                            if len(parts) < 2:
                                continue
                            participant1 = parts[0].strip()
                            participant2 = parts[1].strip()
                            match_id = insert_match(cursor, match_name, participant1, participant2, match_data['url'], league_id)
                            for bet_type, bet_selections in match_data['bets']:
                                if bet_type in bet_type_mapping:
                                    bet_id = insert_bet(cursor, match_id, bet_type_mapping[bet_type].value)
                                    for selection in bet_selections:
                                        option_name = selection[0].replace(',', '.')
                                        arg = str(re.search(pattern, option_name))
                                        option_type = OptionTypes.MORE.value
                                        if re.search('mais', option_name, re.IGNORECASE):
                                            option_name = selection_standardization['more'] + arg
                                        elif re.search('menos', option_name, re.IGNORECASE):
                                            option_type = OptionTypes.LESS.value
                                            option_name = selection_standardization['less'] + arg
                                        elif re.search('sim', option_name, re.IGNORECASE):
                                            option_type = OptionTypes.YES.value
                                        elif re.search('não', option_name, re.IGNORECASE):
                                            option_type = OptionTypes.NO.value
                                        elif re.search(participant1, option_name, re.IGNORECASE):
                                            option_type = OptionTypes.PART1.value
                                        elif re.search(participant2, option_name, re.IGNORECASE):
                                            option_type = OptionTypes.PART2.value
                                        option_id = insert_option(cursor, option_name, selection[1], get_option_type(cursor, option_type), bet_id, )
                    conn.commit()

folder_path = 'src/output'
file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)]
pattern = re.compile('([0-9]*[.])?[0-9]+')
all_data = insert_data(file_paths)
# all_data = insert_data(file_paths[:1]) 
# all_data = load_data(file_paths[1:2])
# all_data = load_data(file_paths[2:3])
# all_data = load_data(file_paths[3:4])
# all_data = "\n".join(name for name in all_data)

# with open('./src/process_bets/data.json', 'w', encoding='utf-8') as file:
#     json.dump(all_data, file, ensure_ascii=False, indent=2)
    
# with open('./src/process_bets/data.json', 'w', encoding='utf-8') as file:
#     file.write(all_data)
