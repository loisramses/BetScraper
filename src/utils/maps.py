from utils.my_types import BetTypes, OptionTypes
       
bet_type_mapping = {
    'Ambas Equipas Marcam': BetTypes.BOTH_TEAMS_SCORE,
    'Ambas as Equipas Marcam': BetTypes.BOTH_TEAMS_SCORE,
    'Ambas as equipas marcam': BetTypes.BOTH_TEAMS_SCORE,
    'Ambas as equipas marcam golo': BetTypes.BOTH_TEAMS_SCORE,
    'Totais': BetTypes.TOTAL_POINTS_MORE_LESS,
    'Total golos': BetTypes.TOTAL_POINTS_MORE_LESS,
    'Total de Golos': BetTypes.TOTAL_POINTS_MORE_LESS,
    'Total de Pontos': BetTypes.TOTAL_POINTS_MORE_LESS,
    'Total de Golos Mais/Menos': BetTypes.TOTAL_POINTS_MORE_LESS,
    'Total de Pontos Mais/Menos': BetTypes.TOTAL_POINTS_MORE_LESS,
    'Quantos pontos serão marcados ao todo?': BetTypes.TOTAL_POINTS_MORE_LESS,
    'Total de Golos Mais/Menos (alternativas)': BetTypes.TOTAL_POINTS_MORE_LESS,
    'Total de Pontos (incluindo prolongamento)': BetTypes.TOTAL_POINTS_MORE_LESS,
    'Total cantos': BetTypes.CORNERS_MORE_LESS,
    'Cantos Mais/Menos': BetTypes.CORNERS_MORE_LESS,
    'Vencedor': BetTypes.WINNER,
    'Vencedor do jogo': BetTypes.WINNER,
    'Vencedor do Jogo': BetTypes.WINNER,
    'Linha de Dinheiro': BetTypes.WINNER,
    'Vencedor (incluindo prolongamento)': BetTypes.WINNER,
    'Jogos': BetTypes.NUMBER_OF_GAMES_MORE_LESS,
    'Total jogos': BetTypes.NUMBER_OF_GAMES_MORE_LESS,
    'Total de Jogos': BetTypes.NUMBER_OF_GAMES_MORE_LESS,
    'Ambos os jogadores ganharão um set': BetTypes.BOTH_PLAYERS_WIN_A_SET,
    'Número total de touchdowns marcados no jogo': BetTypes.TOTAL_TOUCHDOWNS_MORE_LESS,
}

oposing_bets = {
    OptionTypes.MORE: OptionTypes.LESS,
    OptionTypes.LESS: OptionTypes.MORE,
    OptionTypes.YES: OptionTypes.NO,
    OptionTypes.NO: OptionTypes.YES,
    OptionTypes.PART1: OptionTypes.PART2,
    OptionTypes.PART2: OptionTypes.PART1,
}

allowed_sports = ['Futebol', 'Basquetebol', 'Voleibol', 'Ténis', 'Futebol Americano', 'Andebol']
allowed_bookmakers = ['Betano', 'Bwin', 'CasinoPT', 'Lebull']
