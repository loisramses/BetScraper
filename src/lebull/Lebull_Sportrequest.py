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

async def get_events_data(id: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        data = await request_data(f'https://sportsbook-betting-prod.gtdevteam.work/sports/{id}/leagues/upcoming?leagueTimeFilter=10&languageId=14&isStakeGrouped=true&checkIsActive=true', request_options)
        sport = defaultdict(lambda: defaultdict(list))
        for league in data:
            sport_name = league['sportName']
            league_name = league['leagueName']
            for game in league['games']:
                event = defaultdict(lambda: defaultdict(list))
                match_name = f'{game['teamA']} : {game['teamB']}'
                match_url = f'https://www.lebull.pt/?page=/event/{game['eventId']}'
                bets = []
                for bet in game['stakeTypes']:
                    bet_name = bet['stakeTypeName']
                    options = []
                    for option in bet['stakes']:
                        option_name = option['stakeName']
                        if option['stakeArgument']:
                            option_name += f' {str(option['stakeArgument'])}'
                        option_odd = option['betFactor']
                        options.append((option_name, option_odd))
                    bets.append((bet_name, options))
                event[match_name] = defaultdict(lambda: defaultdict(list))
                event[match_name]['url'] = match_url
                event[match_name]['bets'] = bets
                sport[sport_name][league_name].append(event)
        return sport

async def get_all_data():
    sports_data = await request_data('https://sportsbook-betting-prod.gtdevteam.work/sports?languageId=14', request_options)
    sports = defaultdict(lambda: defaultdict(list))
    semaphore = asyncio.Semaphore(6)
    tasks = [get_events_data(sport['sportId'], semaphore) for sport in sports_data['sports']]
    events_data = await asyncio.gather(*tasks)
    for sport in events_data:
        sports.update(sport)
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
    result = await get_all_data()
    with open('./output/lebull_data.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
        
    await browser.stop()

if __name__ == "__main__":
    zd.loop().run_until_complete(main())
    