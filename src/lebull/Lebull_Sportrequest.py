import asyncio
import json
import zendriver as zd
from collections import defaultdict
from rich import print

async def request_data(fetch_url: str, request_options: dict) -> dict:
    script = f"""
    fetch('{fetch_url}', {request_options}).then(response => response.json()).catch((error) => console.error(error))
    """
    return await page.evaluate(script, await_promise=True)

async def get_sports():
    data = await request_data('https://sportsbook-betting-prod.gtdevteam.work/sports?languageId=14', request_options)
    sports = defaultdict(lambda: defaultdict(list))
    for sport in data['sports']:
        sport_name = sport['sportName']
        for country in sport['countries']:
            for league in country['leagues']:
                sports[sport_name].update({league['leagueName']: league['leagueId']}) # change this
    print(sport_name)
    return sports

async def main():
    global page
    global request_options
    browser = await zd.start()
    page = await browser.get('about:blank')

    request_options = {
        'method': 'GET',
        'headers': {
            'X-Auth-Tenant-Id': '126dc7bf-288b-4f72-9536-3aa54648c0f4'
        }
    }
    result = await get_sports()
    print(result)
    # with open('./src/betano/data.json', 'w', encoding='utf-8') as file:
    #     json.dump(result, file, ensure_ascii=False, indent=2)
        
    await browser.stop()

if __name__ == "__main__":
    zd.loop().run_until_complete(main())
    