import zendriver
import asyncio
import json
from utils.helper import request_data
from utils.maps import allowed_sports
from collections import defaultdict

class Lebull_Request:
    def __init__(self, page: zendriver.Tab):
        self.request_options = {
            'method': 'GET',
            'headers': {
                'X-Auth-Tenant-Id': '126dc7bf-288b-4f72-9536-3aa54648c0f4'
            }
        }
        self.page = page

    async def get_events_data(self, id: str, semaphore: asyncio.Semaphore):
        async with semaphore:
            data = await request_data(f'https://sportsbook-betting-prod.gtdevteam.work/sports/{id}/leagues/upcoming?leagueTimeFilter=10&languageId=14&isStakeGrouped=true&checkIsActive=true', self.request_options, self.page)
            sport = defaultdict(lambda: defaultdict(list))
            if not data:
                return sport
            for league in data:
                sport_name = league['sportName']
                league_name = league['leagueName']
                for game in league['games']:
                    event = defaultdict(lambda: defaultdict(list))
                    if (sport_name == allowed_sports[1] or sport_name == allowed_sports[4]) and game['eventComment'] == 'Equipa Casa - Equipa Visitante':
                        match_name = f"{game['teamB']} : {game['teamA']}"
                    else:
                        match_name = f"{game['teamA']} : {game['teamB']}"
                    # match_name = f"{game['teamA']} : {game['teamB']}"
                    match_url = f"https://www.lebull.pt/?page=/event/{game['eventId']}"
                    bets = []
                    for bet in game['stakeTypes']:
                        bet_name = bet['stakeTypeName']
                        options = []
                        for option in bet['stakes']:
                            option_name = option['stakeName']
                            if option['stakeArgument']:
                                option_name += f" {str(option['stakeArgument'])}"
                            option_odd = option['betFactor']
                            options.append((option_name, option_odd))
                        bets.append((bet_name, options))
                    event[match_name] = defaultdict(lambda: defaultdict(list))
                    event[match_name]['url'] = match_url
                    event[match_name]['bets'] = bets
                    sport[sport_name][league_name].append(event)
            return sport

    async def get_all_data(self):
        sports_data = await request_data('https://sportsbook-betting-prod.gtdevteam.work/sports?languageId=14', self.request_options, self.page)
        sports = defaultdict(lambda: defaultdict(list))
        semaphore = asyncio.Semaphore(6)
        tasks = [self.get_events_data(sport['sportId'], semaphore) for sport in sports_data['sports']]
        events_data = await asyncio.gather(*tasks)
        for sport in events_data:
            sports.update(sport)
        return sports

    async def run(self):
        result = await self.get_all_data()
        # with open('output/Lebull.json', 'w', encoding='utf-8') as file:
        #     json.dump(result, file, ensure_ascii=False, indent=2)
    