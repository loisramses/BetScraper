import re
import enum

class Types(enum.Enum):
    WINNER = 'Vencedor' # TÉNIS, BASQUETEBOL, FUTEBOL AMERICANO, VOLEIBOL
    BOTH_TEAMS_SCORE = 'Ambas as Equipas Marcam' # FUTEBOL
    BOTH_PLAYERS_WIN_A_SET = 'Ambos os Jogadores Ganharão 1 Set' # TÉNIS
    TOTAL_POINTS_MORE_LESS = 'Total de Pontos/Golos Mais/Menos' # FUTEBOL, ANDEBOL, BASQUETEBOL, FUTEBOL AMERICANO, VOLEIBOL
    TOTAL_TOUCHDOWNS_MORE_LESS = 'Total de Touchdowns Mais/Menos' # FUTEBOL AMERICANO
    NUMBER_OF_GAMES_MORE_LESS = 'Número de Jogos Mais/Menos' # TÉNIS
    CORNERS_MORE_LESS = 'Cantos Mais/Menos' # FUTEBOL
    
    # BOTH_TEAMS_SCORE_OR_MORE_LESS = 'Ambas as Equipas Marcam OU Mais/Menos' # FUTEBOL
    # TOTAL DE PONTOS PAR OU IMPAR - VER PARA QUAIS DESPORTOS DÁ E 
    # SE VALE A PENA VER ENTRE TODAS AS CASAS DE APOSTAS
    # EMPATE ANULA TAMBÉM É BOM
        
bet_type_mapping = {
    'Ambas Equipas Marcam': Types.BOTH_TEAMS_SCORE,
    'Ambas as Equipas Marcam': Types.BOTH_TEAMS_SCORE,
    'Ambas as equipas marcam': Types.BOTH_TEAMS_SCORE,
    'Ambas as equipas marcam golo': Types.BOTH_TEAMS_SCORE,
    'Totais': Types.TOTAL_POINTS_MORE_LESS,
    'Total golos': Types.TOTAL_POINTS_MORE_LESS,
    'Total de Golos': Types.TOTAL_POINTS_MORE_LESS,
    'Total de Pontos': Types.TOTAL_POINTS_MORE_LESS,
    'Total de Golos Mais/Menos': Types.TOTAL_POINTS_MORE_LESS,
    'Total de Pontos Mais/Menos': Types.TOTAL_POINTS_MORE_LESS,
    'Quantos pontos serão marcados ao todo?': Types.TOTAL_POINTS_MORE_LESS,
    'Total de Golos Mais/Menos (alternativas)': Types.TOTAL_POINTS_MORE_LESS,
    'Total de Pontos (incluindo prolongamento)': Types.TOTAL_POINTS_MORE_LESS,
    'Total cantos': Types.CORNERS_MORE_LESS,
    'Cantos Mais/Menos': Types.CORNERS_MORE_LESS,
    'Vencedor': Types.WINNER,
    'Vencedor do jogo': Types.WINNER,
    'Vencedor do Jogo': Types.WINNER,
    'Linha de Dinheiro': Types.WINNER,
    'Vencedor (incluindo prolongamento)': Types.WINNER,
    'Jogos': Types.NUMBER_OF_GAMES_MORE_LESS,
    'Total jogos': Types.NUMBER_OF_GAMES_MORE_LESS,
    'Total de Jogos': Types.NUMBER_OF_GAMES_MORE_LESS,
    'Ambos os jogadores ganharão um set': Types.BOTH_PLAYERS_WIN_A_SET,
    'Número total de touchdowns marcados no jogo': Types.TOTAL_TOUCHDOWNS_MORE_LESS,
}

selection_normalization = {
    # sub every "," for ".", change the beginning of the bet_name for a normalized one
    'more': 'Mais de ',
    'less': 'Menos de '
}

women_mapping = {
    'Feminino': ['']
}

match_mapping = {
    'to_delete': re.compile(r'\b(fc|sk|club|ac|csc|csm|cs|fk|cp|cd|s\.c\.|sc|sl|sad|sfc|cf|afc| : oaf|as|ssv|sv|1\.|spvgg|tsv|lb|fcv|kv|kvc|ksv|rfc|kas|ksc|pfc|pofc|nk|hnk|gnk|hk|hc|bm)\s')
}