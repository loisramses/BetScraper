import itertools
import json
import os
import re
from rapidfuzz import fuzz, utils
from utils.db_manager import *
from utils.standards import *
from utils.my_types import *
from utils.maps import *
from rich import print

def insert_data(conn: sqlite3.Connection):
    folder_path = 'src/output'
    file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)]
    pattern = re.compile('([0-9]*[.])?[0-9]+')
    cursor = conn.cursor()
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            data = json.load(f)
            for sport_name, leagues in data.items():
                sport_id = get_sport_by_name(cursor, sport_name)
                if not sport_id:
                    continue
                for _, matches in leagues.items():
                    for match in matches:
                        for match_name, match_data in match.items():
                            parts = match_name.split(":")
                            if len(parts) < 2 or not match_data['bets']:
                                continue
                            participant1 = parts[0].strip()
                            participant2 = parts[1].strip()
                            match_id = insert_match(cursor, match_name, participant1, participant2, match_data['url'], sport_id)
                            for bet_type, bet_selections in match_data['bets']:
                                if bet_type in bet_type_mapping:
                                    bet_id = insert_bet(cursor, match_id, bet_type_mapping[bet_type].value)
                                    for selection in bet_selections:
                                        option_name = selection[0].replace(',', '.')
                                        search_result = re.search(pattern, option_name)
                                        arg = search_result.group(0) if search_result else None
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
                                        elif participant1 == option_name:
                                            option_type = OptionTypes.PART1.value
                                        elif participant2 == option_name:
                                            option_type = OptionTypes.PART2.value
                                        option_id = insert_option(cursor, option_name, selection[1], get_option_type_by_option_type(cursor, option_type), bet_id, arg)
                    conn.commit()

def build_pairs(conn: sqlite3.Connection):
    cursor = conn.cursor()
    all_matches = get_all_matches(cursor, "id, name")
    for a, b in itertools.combinations(all_matches, 2):
        id_a, match_name_a = a
        id_b, match_name_b = b
        ratio = fuzz.ratio(match_name_a, match_name_b, processor=utils.default_process) + fuzz.token_set_ratio(match_name_a, match_name_b, processor=utils.default_process)
        if ratio >= 140:
            insert_pair(cursor, id_a, id_b, ratio)
    conn.commit()
            
conn = get_connection('database.db')
init_db(conn)
all_data = insert_data(conn)
build_pairs(conn)
close_connection(conn)


# with open('./src/process_bets/data.json', 'w', encoding='utf-8') as file:
#     json.dump(all_data, file, ensure_ascii=False, indent=2)
    
# with open('./src/process_bets/data.json', 'w', encoding='utf-8') as file:
#     file.write(all_data)
