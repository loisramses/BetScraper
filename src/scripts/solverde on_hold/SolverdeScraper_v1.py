import json
import timeit
# import nodriver as uc
import zendriver
from rich import print
import asyncio
# url for the games is https://www.estorilsolcasinos.pt/pt/apostas/event/{sportId}/0/{leagueId}/{matchId}

async def get_all_sports(page: zendriver.Tab) -> list:
    # sports_e = await page.select_all('a[href^="/apostas/sports/"]')
    sports_e = await page.select_all('a.ta-SportItem')
    sports = []

    # TO EXCLUDE DUMB SPORTS
    for e in sports_e:
        sport_name = e.children[1].text
        if sport_name == 'Desportos de Inverno' or sport_name == 'Motorizados' or sport_name == 'Rugby Union':
            continue
        sport_url = e['href']
        sports.append((sport_name, sport_url))
    return sports
    # return [(e.children[1].text, e['href']) for e in sports_e]

async def get_option(element: zendriver.Element) -> tuple[str, str]:
    option_name = element.children[0].text
    option_odd = element.children[1].text
    return (option_name, option_odd)

async def get_all_options(element: zendriver.Element):
    options = []
    for col in element.children:
        for child in col.children:
            options.append(await get_option(child))
    return options

async def get_all_bets(page: zendriver.Tab):
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

async def get_event_bets(url: str, browser: zendriver.Browser, semaphore: asyncio.Semaphore) -> list:
    async with semaphore:    
        page = await browser.get(url, new_window=True)
        bets = None
        try:
            bets = await get_all_bets(page)
        except:
            pass
        await page.close()
        return bets

async def get_all_events_bets(events: list, browser: zendriver.Browser) -> list:
    semaphore = asyncio.Semaphore(3)
    tasks = [get_event_bets(event[1], browser, semaphore) for event in events]
    all_bets = await asyncio.gather(*tasks)
    # browser.stop()
    flattened_bets = []
    for bets in all_bets:
        if bets:
            flattened_bets.append(bets)
    return flattened_bets

async def get_league_data(page: zendriver.Tab) -> dict:
    data = {}
    try:
        await open_dropdown(page, '.ta-EventListGroup')
    except:
        return {}
    league_blocks_e = await page.select_all('.ta-EventListGroup')
    for league_block in league_blocks_e:
        league_name = league_block.children[0].children[0].children[1].children[0].children[0].text
        if league_name not in data:
            data[league_name] = []
        for event in league_block.children[1].children[0].children[0].children:
            event_url = event.children[1].children[0].attrs['href']
            event_id = event_url.split('/')[-1]
            event_url = f'{base_url}{event_url}'
            data[league_name].append((event_id, event_url))
    return data

async def get_sport_league_data(sport: tuple[str, str], browser: zendriver.Browser, semaphore: asyncio.Semaphore) -> dict:
    async with semaphore:
        data = {}
        full_url = f'{base_url}{sport[1]}/matches/48h'
        page = await browser.get(full_url, new_window=True)
        data[sport[0]] = await get_league_data(page)
        await page.close()
        return data

async def get_all_sport_league_data(browser: zendriver.Browser, sports: list) -> dict:
    semaphore = asyncio.Semaphore(3)
    tasks = [get_sport_league_data(sport, browser, semaphore) for sport in sports]
    all_data = await asyncio.gather(*tasks)
    flattened_data = {}
    for data in all_data:
        flattened_data.update(data.items())
    return flattened_data
    
async def open_dropdown(page: zendriver.Tab, selector: str):
    tabs = await page.select_all(selector, timeout=20)
    for tab in tabs:
        if tab.child_node_count == 1:
            await tab.children[0].click()
    await page.wait(0.1)

async def main():
    global base_url
    base_url = "https://www.solverde.pt"
    # browser = await zendriver.start()
    browser = await zendriver.start(headless=True)
    page = await browser.get(base_url + "/apostas", new_tab=True)
    sports = await get_all_sports(page)
    data = await get_all_sport_league_data(page, sports[:1])
    print(data)
    for sport, leagues in data.items():
        for league, events in leagues.items():
            # print(f'checking {events}')
            data[sport][league] = await get_all_events_bets(events, browser)
    
    # with open('mid-data.json', 'w', encoding='utf-8') as file:
    #     json.dump(data, file, ensure_ascii=False, indent=4)
        
    # for sport, leagues in data.items():
    #     for league, events in leagues.items():
    #         print(f'checking {events}')
    #         data[sport][league] = await get_all_events_bets(events, browser)

    # with open('dados_apostas.json', 'w', encoding='utf-8') as file:
    #     json.dump(data, file, ensure_ascii=False, indent=4)        

if __name__ == "__main__":
    # duration = timeit.timeit(lambda: asyncio.run(main()), number=1)
    # print(duration)
    asyncio.run(main())
