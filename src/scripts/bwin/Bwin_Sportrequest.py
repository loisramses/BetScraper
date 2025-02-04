import zendriver
import json
import re
from datetime import datetime, timedelta, timezone
from utils.helper import request_data
from collections import defaultdict

class Bwin_Request:
    def __init__(self, page: zendriver.Tab):
        self.event_base_url = 'https://sports.bwin.pt/pt/sports/eventos/'
        self.page = page

    def format_date(self, date):
        return date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

    async def get_matches_data(self, sports_list: list) -> dict:
        current_date = datetime.now(timezone.utc)
        time_interval = self.format_date(current_date + timedelta(days=7))
        current_date = self.format_date(current_date)
        ids_string = ",".join(str(sport[1]) for sport in sports_list)
        quantity = 3000
        
        data = await request_data(f'https://sports.bwin.pt/cds-api/bettingoffer/fixtures?x-bwin-accessid=YmQwNTFkNDAtNzM3Yi00YWIyLThkNDYtYWFmNGY2N2Y1OWIx&lang=pt&country=PT&sportIds={ids_string}&take={quantity}&sortBy=FixtureStage&from={current_date}&to={time_interval}&offerMapping=All',
                                {'method': 'GET',
                                'headers': {'Content-Type': 'application/json'}
                                }, self.page)

        sports = defaultdict(lambda: defaultdict(list))
        pattern = re.compile(r'[^\w\s]')
        for entry in data['fixtures']:
            sport_name = entry['sport']['name']['value']
            league_name = entry['competition']['name']['value']

            event = defaultdict(lambda: defaultdict(list))
            event_time = datetime.strptime(entry['startDate'], "%Y-%m-%dT%H:%M:%SZ").strftime('%Y-%m-%d %H:%M:%S')
            match_name = entry['name']['value'].replace(' - ', ' : ')
            event_name_url = '-'.join(re.sub(pattern, '', match_name.lower()).split())
            match_url = f"{self.event_base_url}{event_name_url}-{entry['id']}/?market=-1"
            bets = []
            for bet in entry['optionMarkets']:
                bet_name = bet['name']['value']
                options = []
                for option in bet['options']:
                    option_name = option['name']['value']
                    option_odd = option['price']['odds']
                    options.append((option_name, option_odd))
                bets.append((bet_name, options))
            for bet in entry['games']:
                bet_name = bet['name']['value']
                options = []
                for option in bet['results']:
                    option_name = option['name']['value']
                    option_odd = option['odds']
                    options.append((option_name, option_odd))
                bets.append((bet_name, options))
            event[match_name] = defaultdict(lambda: defaultdict(list))
            event[match_name]['event_time'] = event_time
            event[match_name]['url'] = match_url
            event[match_name]['bets'] = bets
            sports[sport_name][league_name].append(event)
        return sports
            
    async def get_sports_data(self) -> list:
        data = await request_data(
            'https://sports.bwin.pt/cds-api/bettingoffer/counts-batch?x-bwin-accessid=YmQwNTFkNDAtNzM3Yi00YWIyLThkNDYtYWFmNGY2N2Y1OWIx&lang=pt&country=PT',
            {'method': 'POST',
            'headers': {
                'Content-Type': 'application/json',
            },
            'body': json.dumps([{"batchId":"all","request":{"tagTypes":"Sport"}}])
            }, self.page)
        return [(sport['tag']['name']['value'], sport['tag']['id']) for sport in data['all']]

    async def run(self):
        sports = await self.get_sports_data()
        result = await self.get_matches_data(sports)
        with open('output/Bwin.json', 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=2)
