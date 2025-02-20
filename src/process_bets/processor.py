import itertools
import requests
import logging
import json
import os
import re
from rapidfuzz import fuzz
from rapidfuzz.utils import default_process
from utils.db_manager import *
from utils.standards import *
from utils.my_types import *
from utils.maps import *
from rich import print

def calculate_advantage(odd1: float, odd2: float) -> float:
    return 100 - (100/odd1 + 100/odd2)

def calculate_middle(odd1: float, type1: OptionType, arg1: float, odd2: float, type2: OptionType, arg2: float) -> float:
    start = arg1 if type1 == OptionType.MORE else arg2
    end = arg2 if type2 == OptionType.LESS else arg1
    
    # if there's a bad margin to win, just return
    if end - start <= 2:
        return None
    
    t = 100
    s1 = (t * odd2)/(odd1 + odd2)
    s2 = (t * odd1)/(odd1 + odd2)
    advantage = s1 * odd1 + s2 * odd2 - 100
    loss = t - min(s1 * odd1, s2 * odd2)
    return advantage, loss

def insert_data(conn: sqlite3.Connection):
    folder_path = 'output'
    file_paths = [(os.path.join(folder_path, file_name), file_name) for file_name in os.listdir(folder_path)]
    pattern = re.compile('([0-9]*[.])?[0-9]+')
    cursor = conn.cursor()
    for file_path, file_name in file_paths:
        bookmaker_id = get_bookmaker_by_name(cursor, file_name.split('.')[0])
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
                            match_id = insert_match(cursor, match_name, participant1, participant2, match_data['url'], match_data['event_time'], sport_id, bookmaker_id)
                            for bet_type, bet_selections in match_data['bets']:
                                if bet_type in bet_type_mapping:
                                    bet_id = insert_bet(cursor, match_id, get_bet_type_by_bet_type(cursor, bet_type_mapping[bet_type].value))
                                    for selection in bet_selections:
                                        option_name = selection[0].replace(',', '.')
                                        search_result = re.search(pattern, option_name)
                                        arg = search_result.group(0) if search_result else None
                                        option_type = OptionType.MORE.value
                                        if re.search('mais', option_name, re.IGNORECASE):
                                            option_name = selection_standardization['more'] + arg
                                        elif re.search('menos', option_name, re.IGNORECASE):
                                            option_type = OptionType.LESS.value
                                            option_name = selection_standardization['less'] + arg
                                        elif re.search('sim', option_name, re.IGNORECASE):
                                            option_type = OptionType.YES.value
                                            option_name = "Sim"
                                        elif re.search('não', option_name, re.IGNORECASE):
                                            option_type = OptionType.NO.value
                                            option_name = "Não"
                                        elif participant1 == option_name or fuzz.token_ratio(participant1, option_name, processor=default_process) > 85:
                                            option_type = OptionType.PART1.value
                                        elif participant2 == option_name or fuzz.token_ratio(participant2, option_name, processor=default_process) > 85:
                                            option_type = OptionType.PART2.value
                                        option_id = insert_option(cursor, option_name, selection[1], get_option_type_by_option_type(cursor, option_type), bet_id, arg)
                    conn.commit()

def build_pairs(conn: sqlite3.Connection):
    cursor = conn.cursor()
    all_matches = get_all_matches(cursor, "id, name, participant1, participant2, start_time, sport_id, bookmaker_id")
    for a, b in itertools.combinations(all_matches, 2):
        id_a, match_name_a, part1_a, part2_a, start_time_a, sport_id_a, bookmaker_id_a = a
        id_b, match_name_b, part1_b, part2_b, start_time_b,  sport_id_b, bookmaker_id_b = b
        sort_ratio = fuzz.ratio(match_name_a, match_name_b)
        parts_ratio = (fuzz.token_ratio(part1_a, part1_b) + fuzz.token_ratio(part2_a, part2_b)) / 2
        ratio = (parts_ratio + sort_ratio) / 2
        if ratio >= 70 and start_time_a == start_time_b and sport_id_a == sport_id_b and bookmaker_id_a != bookmaker_id_b:
            insert_pair(cursor, id_a, id_b, ratio)
    conn.commit()

def build_opportunities(conn: sqlite3.Connection):
    cursor = conn.cursor()
    all_pairs = get_all_pairs(cursor, "id, match1_id, match2_id")
    for pair in all_pairs:
        pair_id, match_id_a, match_id_b = pair
        options_match_a = get_options_by_match_id(cursor, match_id_a)
        options_match_b = get_options_by_match_id(cursor, match_id_b)
        if not options_match_a or not options_match_b:
            continue
        for option_a in options_match_a:
            option_id_a, option_type_name_a, option_arg_a, option_odd_a, bet_type_a = option_a
            option_type_name_a = OptionType(option_type_name_a)
            bet_type_a = BetType(bet_type_a)
            for option_b in options_match_b:
                option_id_b, option_type_name_b, option_arg_b, option_odd_b, bet_type_b = option_b
                option_type_name_b = OptionType(option_type_name_b)
                bet_type_b = BetType(bet_type_b)
                if bet_type_a == bet_type_b and option_type_name_b == oposing_bets[option_type_name_a]:
                    if option_arg_a == option_arg_b:
                        advantage = calculate_advantage(option_odd_a, option_odd_b)
                        insert_oportunity(cursor, 'advantage', option_id_a, option_id_b, advantage, pair_id)
                    elif option_arg_a is not None and option_arg_b is not None:
                        result = calculate_middle(option_odd_a, option_type_name_a, option_arg_a, option_odd_b, option_type_name_b, option_arg_b)
                        if result is not None:
                            possible_gain, possible_loss = result
                            insert_oportunity(cursor, 'middle', option_id_a, option_id_b, possible_gain, pair_id, possible_loss)
                        
    conn.commit()

def send_message(oportunity):
    match_name, url1, url2, bet_type, option1, odd1, option2, odd2, advantage, trust_factor, oportunity_type, possible_loss = oportunity
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    match_name = match_name.replace('(', '\\(').replace(')', '\\)')
    option1 = option1.replace('(', '\\(').replace(')', '\\)').replace('.', '\\.')
    url1 = url1.replace('-', '\\-')
    odd1 = str(odd1).replace('.', '\\.')
    option2 = option2.replace('(', '\\(').replace(')', '\\)').replace('.', '\\.')
    url2 = url2.replace('-', '\\-')
    odd2 = str(odd2).replace('.', '\\.')
    advantage = str(advantage).replace('.', '\\.')
    trust_factor = str(trust_factor).replace('.', '\\.')
    
    # TODO: add condition on oportunity type
    if oportunity_type == 'advantage':    
        message = f"""
        *Oportunidade ARBITRAGE*
        *{match_name}*
        *Tipo de aposta:* {bet_type}
        *1ª opção:* [{option1}]({url1}) *Odd:* {odd1}
        *2ª opção:* [{option2}]({url2}) *Odd:* {odd2}
        *Percentagem:* {advantage}
        *Taxa de confiança da relação entre jogos:* {trust_factor}
        """
    else:
        message = f"""
        *Oportunidade MIDDLE*
        *{match_name}*
        *Tipo de aposta:* {bet_type}
        *1ª opção:* [{option1}]({url1}) *Odd:* {odd1}
        *2ª opção:* [{option2}]({url2}) *Odd:* {odd2}
        *Potenciais Ganhos:* {advantage}
        *Potenciais Perdas:* {possible_loss}
        *Taxa de confiança da relação entre jogos:* {trust_factor}
        """
        
    # print(message)
    logging.warning(message)
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "MarkdownV2", "link_preview_options": {"is_disabled": True}}
    response = requests.post(url, json=payload)
    logging.warning(response._content)
    # print(response._content)

def expose_bets(conn: sqlite3.Connection):
    cursor = conn.cursor()
    all_oportunities = get_oportunities_for_export(cursor)
    if not all_oportunities: return
    for oportunity in all_oportunities:
        send_message(oportunity)

conn = get_connection('../database.db')
logging.basicConfig(filename="logs/log.log", filemode='a', format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
init_db(conn)
clean_up_db(conn)
logging.info("Inserting data into DB")
insert_data(conn)
logging.info("Building pairs")
build_pairs(conn)
logging.info("Building opportunities")
build_opportunities(conn)
logging.info("Exposing Bets")
expose_bets(conn)
close_connection(conn)
logging.info("Processing Done!")
