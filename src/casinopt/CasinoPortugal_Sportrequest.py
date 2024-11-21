import zendriver as zd
import asyncio
import json
from datetime import datetime, timedelta, timezone
from collections import defaultdict

async def request_data(fetch_url: str, request_options: dict) -> dict:
    script = f"""
    fetch('{fetch_url}', {request_options}).then(response => response.json()).catch((error) => console.error(error))
    """
    return await page.evaluate(script, await_promise=True)

def get_competitor_name(string: str, sport_entry: dict) -> str:
    string = string.replace('{$competitor1}', sport_entry['home_name'])
    string = string.replace('{$competitor2}', sport_entry['away_name'])
    return string

async def get_event_data(event_id: str, semaphore: asyncio.Semaphore) -> list:
    async with semaphore:
        return await request_data(f'{base_url}id={event_id}', {'method': 'GET'})

def process_str(string: str, variables: dict) -> str:
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

async def get_events_data(event_ids: list) -> dict:
    semaphore = asyncio.Semaphore(6)
    tasks = [get_event_data(event, semaphore) for event in event_ids]
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
        match_url = f'{base_url}{entry['id']}'
        bets = []
        for bet in entry['markets']:
            variables = dict(item.split('=') for item in bet['specifiers'].split('&')) if bet['specifiers'] else {}
            bet_name = get_competitor_name(bet['name_pt'], entry) if not variables else process_str(get_competitor_name(bet['name_pt'], entry), variables)
            options = []
            for option in bet['selections']:
                option_name = get_competitor_name(option['name_pt'], entry) if not variables else process_str(get_competitor_name(option['name_pt'], entry), variables)
                option_odd = option['decimal']
                options.append((option_name, option_odd))
            bets.append((bet_name, options))

        event[match_name] = defaultdict(lambda: defaultdict(list))
        event[match_name]['url'] = match_url
        event[match_name]['bets'] = bets
        sports[sport_name][league_name].append(event)
    return sports
        
async def get_event_ids(quantity: int, sportIds: str, days_interval: int) -> list:
    data = await request_data(
        f'{base_url}sportId={sportIds}&take={quantity}',
        {'method': 'GET'}
    )
    
    results = []
    for event in data['fixtures']:
        event_date = datetime.strptime(event['start_time_utc'], '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        current_date = datetime.now(timezone.utc)
        if event_date <= (current_date + timedelta(days=days_interval)):
            results.append(event['id'])
    return results

async def main():
    global event_base_url
    global base_url
    global page
    browser = await zd.start()
    page = await browser.get('about:blank')
    event_base_url = 'https://www.casinoportugal.pt/desportos/mercados/'
    base_url = 'https://odds.casinoportugal.pt/redis/fixtures?'
    # quando for pra meter apenas um ou dois desportos lembrar de meter '%2C' (que significa ',' em ASCII) entre
    # cada desporto
    event_ids = await get_event_ids(quantity=600, sportIds="all", days_interval=2)
 
    result = await get_events_data(event_ids)
    with open('./src/casinopt/data.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
        
    await browser.stop()

if __name__ == "__main__":
    zd.loop().run_until_complete(main())
