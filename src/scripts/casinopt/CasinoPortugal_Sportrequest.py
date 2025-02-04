# import nodriver as uc
import zendriver
import asyncio
import json
from datetime import datetime, timedelta, timezone
from utils.helper import request_data
from collections import defaultdict

class CasinoPT_Request():
    def __init__(self, page: zendriver.Tab):
        self.event_base_url = 'https://www.casinoportugal.pt/desportos/mercados/'
        self.base_url = 'https://odds.casinoportugal.pt/redis/fixtures?'
        self.page = page

    def get_competitor_name(self, string: str, sport_entry: dict) -> str:
        string = string.replace('{$competitor1}', sport_entry['home_name'])
        string = string.replace('{$competitor2}', sport_entry['away_name'])
        return string

    async def get_event_data(self, event_id: str, semaphore: asyncio.Semaphore) -> list:
        async with semaphore:
            return await request_data(f'{self.base_url}id={event_id}', {'method': 'GET'}, self.page)

    def process_str(self, string: str, variables: dict) -> str:
        for key, value in variables.items():
            placeholder_variants = [f"{{{key}}}", f"{{!{key}}}", f"{{+{key}}}", f"{{-{key}}}"]
            for placeholder in placeholder_variants:
                if placeholder in string:
                    if f"+{key}" in placeholder:
                        string = string.replace(placeholder, f"{float(value):+}")
                    elif f"-{key}" in placeholder:
                        string = string.replace(placeholder, f"{-float(value):+}")
                    elif f"!{key}" in placeholder:
                        string = string.replace(placeholder, f"{value}º")
                    else:
                        string = string.replace(placeholder, value)
        return string

    async def get_events_data(self, event_ids: list) -> dict:
        semaphore = asyncio.Semaphore(6)
        tasks = [self.get_event_data(event, semaphore) for event in event_ids]
        all_events = await asyncio.gather(*tasks)

        flattened_events = []
        for entry in all_events:
            flattened_events.extend(entry['fixtures'])

        sports = defaultdict(lambda: defaultdict(list))
        for entry in flattened_events:
            sport_name = entry['sport_name']
            league_name = entry['comp_name']
            event = defaultdict(lambda: defaultdict(list))
            match_name = entry['name'].replace('vs.', ':')
            event_time = entry['start_time_utc']
            match_url = f"{self.event_base_url}{entry['id']}"
            bets = []
            for bet in entry['markets']:
                if bet['trading_status'] == 'Suspended': continue
                variables = dict(item.split('=') for item in bet['specifiers'].split('&')) if bet['specifiers'] else {}
                bet_name = self.get_competitor_name(bet['name_pt'], entry) if not variables else self.process_str(self.get_competitor_name(bet['name_pt'], entry), variables)
                options = []
                for option in bet['selections']:
                    option_name = self.get_competitor_name(option['name_pt'], entry) if not variables else self.process_str(self.get_competitor_name(option['name_pt'], entry), variables)
                    option_odd = option['decimal']
                    options.append((option_name, option_odd))
                bets.append((bet_name, options))

            event[match_name] = defaultdict(lambda: defaultdict(list))
            event[match_name]['event_time'] = event_time
            event[match_name]['url'] = match_url
            event[match_name]['bets'] = bets
            sports[sport_name][league_name].append(event)
        return sports
            
    async def get_event_ids(self, quantity: int, sportIds: str, days_interval: int) -> list:
        data = await request_data(
            f"{self.base_url}sportId={sportIds}&take={quantity}",
            {'method': 'GET'},
            self.page
        )
        
        results = []
        for event in data['fixtures']:
            event_date = datetime.strptime(event['start_time_utc'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
            current_date = datetime.now(timezone.utc)
            if event_date <= (current_date + timedelta(days=days_interval)):
                results.append(event['id'])
        return results

    async def run(self):
        # quando for pra meter apenas um ou dois desportos lembrar de meter '%2C' (que significa ',' em ASCII) entre
        # cada desporto
        event_ids = await self.get_event_ids(quantity=3000, sportIds="all", days_interval=7)
    
        result = await self.get_events_data(event_ids)
        with open('output/CasinoPT.json', 'w', encoding='utf-8') as file:
            json.dump(result, file, ensure_ascii=False, indent=2)
