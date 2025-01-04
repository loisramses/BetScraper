# import nodriver as uc
import zendriver
import asyncio
import json
import re
from rich import print
from datetime import datetime, timedelta, timezone
from collections import defaultdict

async def request_data(fetch_url: str, request_options: dict) -> dict:
    script = f"""
    fetch('{fetch_url}', {request_options}).then(response => response.json()).catch((error) => console.error(error))
    """
    return await page.evaluate(script, await_promise=True)
        
def format_date(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

def get_matches_data(data:dict) -> dict:
    # sports = defaultdict(lambda: defaultdict(list))
    # pattern = re.compile(r'[^\w\s]')
    # for entry in data['fixtures']:
    #     sport_name = entry['sport']['name']['value']
    #     league_name = entry['competition']['name']['value']

    #     event = defaultdict(lambda: defaultdict(list))
    #     match_name = entry['name']['value']
    #     event_name_url = '-'.join(re.sub(pattern, '', match_name.lower()).split())
    #     match_url = f'{event_base_url}{event_name_url}-{entry['id']}/?market=-1'
    #     bets = []
    #     for bet in entry['optionMarkets']:
    #         bet_name = bet['name']['value']
    #         options = []
    #         for option in bet['options']:
    #             option_name = option['name']['value']
    #             option_odd = option['price']['odds']
    #             options.append((option_name, option_odd))
    #         bets.append((bet_name, options))
    #     for bet in entry['games']:
    #         bet_name = bet['name']['value']
    #         options = []
    #         for option in bet['results']:
    #             option_name = option['name']['value']
    #             option_odd = option['odds']
    #             options.append((option_name, option_odd))
    #         bets.append((bet_name, options))
    #     event[match_name] = defaultdict(lambda: defaultdict(list))
    #     event[match_name]['url'] = match_url
    #     event[match_name]['bets'] = bets
    #     sports[sport_name][league_name].append(event)
    # return sports
    pass
        
async def get_sports_data() -> list:
    await page.wait(20)
    data = await request_data('https://offer.cdn.begmedia.com/api/pub/v3/sports?application=1024&language=pt', {'method': 'GET'})
    print(data)
    return [(sport['name'], sport['id']) for sport in data['sports']]

async def main():
    # global event_base_url
    global page
    # browser = await zendriver.start()
    browser = await zendriver.start(headless=True)
    page = await browser.get('about:blank')
    # event_base_url = 'https://sports.bwin.pt/pt/sports/eventos/'
    sports = await get_sports_data()
    print(sports)
    # sports = get_sports_data(await page.evaluate(script, await_promise=True))
    # currentDate = datetime.now(timezone.utc)
    # oneHourLater = format_date(currentDate + timedelta(hours=5))
    # currentDate = format_date(currentDate)
    # ids_string = ",".join(str(sport[1]) for sport in sports)
    # quantity = 30
    
    # script = f"""
    # fetch('https://sports.bwin.pt/cds-api/bettingoffer/fixtures?x-bwin-accessid=YmQwNTFkNDAtNzM3Yi00YWIyLThkNDYtYWFmNGY2N2Y1OWIx&lang=pt&country=PT&sportIds={ids_string}&take={quantity}&sortBy=FixtureStage&from={currentDate}&to={oneHourLater}&offerMapping=All', {{
    #     method: 'GET',
    #     headers: {{
    #         'Content-Type': 'application/json',
    #     }}
    # }}).then(response => response.json()).catch((error) => console.error(error))
    # """
    # data = await page.evaluate(script, await_promise=True)
    # result = get_matches_data(data)
    # with open('bwin/data.json', 'w', encoding='utf-8') as file:
    #     json.dump(result, file, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    asyncio.run(main())
