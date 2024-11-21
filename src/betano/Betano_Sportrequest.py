import zendriver as zd
from collections import defaultdict
from rich import print

async def request_data(fetch_url: str, request_options: dict) -> dict:
    script = f"""
    fetch('{fetch_url}', {request_options}).then(response => response.json()).catch((error) => console.error(error))
    """
    return await page.evaluate(script, await_promise=True)

# TODO: CONCURRENCY

async def get_league_events_and_bets(url: str):
    data = await request_data(f'{base_api_url}{url}', {'method': 'GET'})
    for event in data['data']['blocks'][0]['events']:
        event_name = event['name'].replace('-', ':')
        event_url = f'{base_url}{event['url']}'
        

async def get_sports():
    data = await request_data(
        'https://www.betano.pt/api/sport/futebol/',
        {'method': 'GET'}
    )
    sports = defaultdict(lambda: defaultdict(list))

    for sport in data['structureComponents']['sports']['data']:
        response = await request_data(f'{base_api_url}{sport['url']}', {'method': 'GET'})
        if 'errors' not in response:
            sport_name = sport['name']
            for group in response['data']['regionGroups']:
                for region in group['regions']:
                    for league in region['leagues']:
                        league_name = league['name']
                        league_url = league['url']
                        sports[sport_name][league_name] = await get_league_events_and_bets(league_url)
    return sports

async def main():
    global base_url
    global base_api_url
    global sport_base_url
    global page
    browser = await zd.start()
    page = await browser.get('about:blank')
    base_url = 'https://www.betano.pt'
    base_api_url = 'https://www.betano.pt/api'
    sport_base_url = f'{base_api_url}/sport'
    await get_sports()
    await browser.stop()

if __name__ == "__main__":
    zd.loop().run_until_complete(main())