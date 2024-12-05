import enum

class BetTypes(enum.Enum):
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
    
class OptionTypes(enum.Enum):
    MORE = 'Mais de'
    LESS = 'Menos de'
    YES = 'Sim'
    NO = 'Não'
    PART1 = 'Participante 1'
    PART2 = 'Participante 2'