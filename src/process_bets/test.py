import json
from utils.db_manager import *
from utils.standards import *
from utils.maps import oposing_bets
from utils.my_types import OptionTypes
import itertools
from rapidfuzz import fuzz
from rich import print

def calculate_advantage(odd1: float, odd2: float) -> float:
    return 100 - (100/odd1 + 100/odd2)

conn = get_connection('database.db')
cursor = conn.cursor()

# all_matches = get_all_matches(cursor, "id, name, participant1, participant2")
# result = []
# for a, b in itertools.combinations(all_matches, 2):
#     id_a, match_name_a, part1_a, part2_a = a
#     id_b, match_name_b, part1_b, part2_b = b
#     sort_ratio = fuzz.token_sort_ratio(match_name_a, match_name_b)
#     parts_ratio = max(((fuzz.token_ratio(part1_a, part2_b) + fuzz.token_ratio(part2_a, part1_b)) / 2), ((fuzz.token_ratio(part1_a, part1_b) + fuzz.token_ratio(part2_a, part2_b)) / 2))
#     ratio = (parts_ratio + sort_ratio) / 2
#     if ratio >= 30 and ratio <= 50:
#         result.append(((id_a, match_name_a), (id_b, match_name_b), ratio))

evaluated_data = []
all_pairs = get_all_pairs(cursor, "*")
# _, match_id_a, match_id_b, trust_factor = all_pairs[0]
for pair in all_pairs:
    _, match_id_a, match_id_b, trust_factor = pair
    match_name_a = get_match_by_id(cursor, "name", match_id_a)
    match_name_b = get_match_by_id(cursor, "name", match_id_b)
    options_match_a = get_options_by_match_id(cursor, match_id_a)
    options_match_b = get_options_by_match_id(cursor, match_id_b)
    if not options_match_a or not options_match_b:
        continue
    for option_a in options_match_a:
        bet_type_a, option_name_a, option_arg_a, option_odd_a, option_type_name_a, _ = option_a
        option_type_name_a = OptionTypes(option_type_name_a)
        bet_type_a = BetTypes(bet_type_a)

        for option_b in options_match_b:
            bet_type_b, option_name_b, option_arg_b, option_odd_b, option_type_name_b, _ = option_b
            option_type_name_b = OptionTypes(option_type_name_b)
            bet_type_b = BetTypes(bet_type_b)
            if bet_type_a == bet_type_b and option_type_name_b == oposing_bets[option_type_name_a] and option_arg_a == option_arg_b:
                advantage = calculate_advantage(option_odd_a, option_odd_b)
                if trust_factor > 78 and 0 <= advantage:
                    print(match_name_a, match_id_a, match_name_b, match_id_b, bet_type_a, option_name_a, option_odd_a, option_name_b, option_odd_b, advantage)

# with open('./src/process_bets/data.json', 'w', encoding='utf-8') as file:
#     json.dump(result, file, ensure_ascii=False, indent=2)

# conn.commit()
