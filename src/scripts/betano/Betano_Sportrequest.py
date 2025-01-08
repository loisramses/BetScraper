import zendriver
import asyncio
import json
from utils.helper import request_data
from collections import defaultdict

class Betano_Request:
    def __init__(self, page: zendriver.Tab):
        self.page = page
        self.base_url = 'https://www.betano.pt'
        self.base_api_url = 'https://www.betano.pt/api'
        self.sport_base_url = f'{self.base_api_url}/sport'

    async def get_event_bets(self, event: dict, semaphore: asyncio.Semaphore) -> dict:
        async with semaphore:
            data = await request_data(f"{self.base_api_url}{event['url']}", {'method': 'GET'}, self.page)
            bets = []
            event_name = event['name'].replace(' - ', ' : ')
            event_url = f"{self.base_url}{event['url']}"
            try: # avoid live events
                
                for bet in data['data']['event']['markets']:
                    bet_name = bet['name']
                    options = []
                    for option in bet['selections']:
                        option_name = option['name']
                        option_odd = option['price']
                        options.append((option_name, option_odd))
                    if 'tableLayout' in bet:
                        for group_selection in bet['tableLayout']['rows']:
                            for option in group_selection['groupSelections'][0]['selections']:
                                option_name = option['name']
                                option_odd = option['price']
                                options.append((option_name, option_odd))
                    bets.append((bet_name, options))
            except:
                pass
            
            event = defaultdict(lambda: defaultdict(list))
            event[event_name] = {
                'url': event_url,
                'bets': bets
            }
            
            return event

    async def get_league_events_and_bets(self, url: str, league_name: str,  semaphore: asyncio.Semaphore) -> dict | None:
        async with semaphore:
            data = await request_data(f'{self.base_api_url}{url}', {'method': 'GET'}, self.page)
            try:
                if data['data']['blocks']:
                    sema = asyncio.Semaphore(3)
                    tasks = [self.get_event_bets(event, sema) for event in data['data']['blocks'][0]['events']]
                    all_events = await asyncio.gather(*tasks)
                    return { league_name: all_events}
                else:
                    return None
            except Exception:
                pass

    async def get_sports(self):
        semaphore = asyncio.Semaphore(2)
        data = await request_data(
            'https://www.betano.pt/api/sport/futebol/',
            {'method': 'GET'},
            self.page
        )
        sports = defaultdict(lambda: defaultdict(list))

        for sport in data['structureComponents']['sports']['data']:
            response = await request_data(f"{self.base_api_url}{sport['url']}", {'method': 'GET'}, self.page)
            if 'errors' not in response:
                sport_name = sport['name']
                for group in response['data']['regionGroups']:
                    for region in group['regions']:
                        tasks = [self.get_league_events_and_bets(league['url'], league['name'], semaphore) for league in region['leagues']]
                        all_leagues = await asyncio.gather(*tasks)
                        for item in all_leagues:
                            if item:
                                sports[sport_name].update(item.items())
        return sports

    async def run(self):
        result = await self.get_sports()
        with open('output/Betano.json', 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=2)
