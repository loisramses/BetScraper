from utils.my_types import BetType, OptionType
       
bet_type_mapping = {
    'Ambas Equipas Marcam': BetType.BOTH_TEAMS_SCORE,
    'Ambas as Equipas Marcam': BetType.BOTH_TEAMS_SCORE,
    'Ambas as equipas marcam': BetType.BOTH_TEAMS_SCORE,
    'Ambas as equipas marcam golo': BetType.BOTH_TEAMS_SCORE,
    'Totais': BetType.TOTAL_POINTS_MORE_LESS,
    'Total golos': BetType.TOTAL_POINTS_MORE_LESS,
    'Total de Golos': BetType.TOTAL_POINTS_MORE_LESS,
    'Total de Pontos': BetType.TOTAL_POINTS_MORE_LESS,
    'Total de Golos Mais/Menos': BetType.TOTAL_POINTS_MORE_LESS,
    'Total de Pontos Mais/Menos': BetType.TOTAL_POINTS_MORE_LESS,
    'Quantos pontos serão marcados ao todo?': BetType.TOTAL_POINTS_MORE_LESS,
    'Total de Golos Mais/Menos (alternativas)': BetType.TOTAL_POINTS_MORE_LESS,
    'Total de Pontos (incluindo prolongamento)': BetType.TOTAL_POINTS_MORE_LESS,
    'Total cantos': BetType.CORNERS_MORE_LESS,
    'Cantos Mais/Menos': BetType.CORNERS_MORE_LESS,
    'Vencedor': BetType.WINNER,
    'Vencedor do jogo': BetType.WINNER,
    'Vencedor do Jogo': BetType.WINNER,
    'Linha de Dinheiro': BetType.WINNER,
    'Vencedor (incluindo prolongamento)': BetType.WINNER,
    'Jogos': BetType.NUMBER_OF_GAMES_MORE_LESS,
    'Total jogos': BetType.NUMBER_OF_GAMES_MORE_LESS,
    'Total de Jogos': BetType.NUMBER_OF_GAMES_MORE_LESS,
    'Ambos os jogadores ganharão um set': BetType.BOTH_PLAYERS_WIN_A_SET,
    'Número total de touchdowns marcados no jogo': BetType.TOTAL_TOUCHDOWNS_MORE_LESS,
}

oposing_bets = {
    OptionType.MORE: OptionType.LESS,
    OptionType.LESS: OptionType.MORE,
    OptionType.YES: OptionType.NO,
    OptionType.NO: OptionType.YES,
    OptionType.PART1: OptionType.PART2,
    OptionType.PART2: OptionType.PART1,
}

allowed_sports = ['Futebol', 'Basquetebol', 'Voleibol', 'Ténis', 'Futebol Americano', 'Andebol']
allowed_bookmakers = ['Betano', 'Bwin', 'CasinoPT', 'Lebull']
