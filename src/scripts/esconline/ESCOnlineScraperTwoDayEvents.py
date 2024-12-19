import json
import timeit
import nodriver as uc
from rich import print
import asyncio
# url for the games is https://www.estorilsolcasinos.pt/pt/apostas/event/{sportId}/0/{leagueId}/{matchId}

async def get_all_sports(page: uc.Tab) -> list:
    await (await page.select('a[data-bind*="$root.moreLessSport"]')).click()
    sports_e = await page.select_all('a[href^="/pt/apostas/desporto/"]')
    return [(e.text, e['href']) for e in sports_e]

async def get_option(element: uc.Element) -> tuple[str, str]:
    option_name = element.children[0].text
    option_odd = element.children[1].text
    return (option_name, option_odd)

async def get_all_options(element: uc.Element):
    options = []
    for col in element.children:
        for child in col.children:
            options.append(await get_option(child))
    return options

async def get_all_bets(page: uc.Tab):
    event = {}
    await (await page.select('.filters__list', timeout=20)).children[1].click()
    event_name = (await page.select('.breadcrumb')).children[1].children[-2].children[-2].text
    event[event_name] = {
        'url': page.url,
        'bets': []
    }
    all_bets_e = await page.select_all('div[id^="MarketId"]')
    for bet in all_bets_e:
        bet_name = bet.children[0].children[1].text
        event[event_name]['bets'].append((bet_name, await get_all_options(bet.children[1])))
    return event

async def get_event_bets(url: str, browser: uc.Browser, semaphore: asyncio.Semaphore) -> list:
    async with semaphore:    
        page = await browser.get(url, new_window=True)
        bets = None
        try:
            bets = await get_all_bets(page)
        except:
            pass
        await page.close()
        return bets

async def get_all_events_bets(events: list, browser: uc.Browser) -> list:
    semaphore = asyncio.Semaphore(3)
    tasks = [get_event_bets(event[1], browser, semaphore) for event in events]
    all_bets = await asyncio.gather(*tasks)
    flattened_bets = []
    for bets in all_bets:
        if bets:
            flattened_bets.append(bets)
    return flattened_bets

async def get_league_data(page: uc.Tab, sport: str, data: dict = None) -> dict:
    event_base_url = "https://www.estorilsolcasinos.pt/pt/apostas/event/"
    if not data:
        data = {}
    while True:
        try:
            await (await page.select('.bet-group-list-show-more', 4)).children[0].click()
        except Exception:
            break
        
    try:
        league_blocks_e = await page.select_all('div.bet-league')
        for league_block in league_blocks_e:
            league_id = league_block.attrs['id'].split('_')[-1]
            league_name = league_block.children[0].children[1].children[0].text
            if league_name not in data:
                data[league_name] = []
            for event in league_block.children[1].children:
                event_id = event.attrs['id'].split('_')[-1]
                event_url = f'{event_base_url}{sport.split('/')[-1]}/0/{league_id}/{event_id}'
                data[league_name].append((event_id, event_url))
    except Exception:
        pass
    return data

async def get_sport_league_data(page: uc.Tab, sports: list) -> dict:
    data = {}
    for sport in sports:
        await (await page.select(f'a[href="{sport[1]}"]')).click()
        data[sport[0]] = await get_league_data(page, sport[1])
        try:
            await (await page.select('.filters__list', timeout=3)).children[2].click()
            data[sport[0]] = await get_league_data(page, sport[1], data[sport[0]])
        except:
            pass
        await (await page.select('li.go-back')).children[0].click()
    return data
        
async def main():
    base_url = "https://www.estorilsolcasinos.pt"
    browser = await uc.start(browser_args=['--start-maximized'])
    page = await browser.get(base_url + "/pt/apostas/", new_tab=True)  # sports betting page
    sports = await get_all_sports(page)
    data = await get_sport_league_data(page, sports)
        
    for sport, leagues in data.items():
        for league, events in leagues.items():
            data[sport][league] = await get_all_events_bets(events, browser)

    await browser.stop()
    with open('esconline/dados_apostas.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)        

if __name__ == "__main__":
    duration = timeit.timeit(lambda: uc.loop().run_until_complete(main()), number=1)
    print(duration)
