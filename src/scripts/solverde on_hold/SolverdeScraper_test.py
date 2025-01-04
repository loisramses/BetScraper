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

    return [(e.children[1].text, e['href']) for e in sports_e]

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
    await (await page.select_all('.ta-ButtonBarItem', timeout=20))[-1].click()
    participants = await page.select_all('STATSCOREWidget--compactH2H__participantName')
    event_name = f'{participants[0]} : {participants[1]}'
    await open_dropdown(page, '.ta-AggregatedMarket')
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
    await open_dropdown(page)

    league_blocks_e = await page.select_all('.ta-EventListGroup')
    for league_block in league_blocks_e:
        league_name = league_block.children[0].children[0].children[1].children[0].children[0].text
        if league_name not in data:
            data[league_name] = []
        for event in league_block.children[1].children[0].children[0].children:
            event_url = event.children[1].children[0].attrs['href']
            event_id = event_url.split('/')[-1]
            event_url = f'{base_site_url}{event_url}'
            data[league_name].append((event_id, event_url))
    
    return data

async def get_sport_league_data(url: str, browser: zendriver.Browser, semaphore: asyncio.Semaphore) -> dict: # falta meter o tipo de retorno
    two_day_url = "/matches/48h"
    async with semaphore:
        page = await browser.get(url + two_day_url, new_tab=True)
        data = await get_league_data(page)
        await page.close()
        return data

async def get_all_sport_league_data(browser: zendriver.Browser, sports: list) -> dict:
    semaphore = asyncio.Semaphore(3)
    tasks = [get_sport_league_data(sport[1], browser, semaphore) for sport in sports]
    all_data = await asyncio.gather(*tasks)
    print(all_data)
    return all_data

async def open_dropdown(page: zendriver.Tab, selector: str):
    tabs = await page.select_all(selector, timeout=20)
    for tab in tabs:
        if tab.child_node_count == 1:
            await tab.children[0].click()
    await page.wait(0.1)
    
async def main():
    global base_site_url
    base_url = "https://www.solverde.pt/apostas/sports/soccer/matches/48h"
    base_site_url = "https://www.solverde.pt"
    # browser = await zendriver.start(browser_args=['--start-maximized'])
    # browser = await zendriver.start()
    browser = await zendriver.start(headless=True)
    page = await browser.get('https://www.solverde.pt/apostas/sports/soccer/events/10157742755', new_tab=True)  # sports betting page
    await (await page.select_all('.ta-ButtonBarItem', timeout=20))[-1].click()
    await browser.wait(20)
    # data = await get_league_data(page)
    events = [('10157742755', 'https://www.solverde.pt/apostas/sports/soccer/events/10157742755'),
            ('10162120860', 'https://www.solverde.pt/apostas/sports/soccer/events/10162120860'),
            ('10162121101', 'https://www.solverde.pt/apostas/sports/soccer/events/10162121101'),
            ('10162433866', 'https://www.solverde.pt/apostas/sports/soccer/events/10162433866'),]
    
    print(await get_all_events_bets(events, browser))
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
