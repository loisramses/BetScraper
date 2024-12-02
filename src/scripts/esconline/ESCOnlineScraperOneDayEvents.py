import nodriver as uc
from rich import print
import time
# url for the games is https://www.estorilsolcasinos.pt/pt/apostas/event/{sportId}/0/{leagueId}/{matchId}

async def get_all_sports(page: uc.Tab) -> list:
    sports_e = await page.select_all('li.Sports')
    return [e.children[0].children[0].text for e in sports_e]

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
    bets = []
    all_bets_e = await page.select_all('div[id^="MarketId"]')
    for bet in all_bets_e:
        bet_name = bet.children[0].children[1].text
        bets.append((bet_name, await get_all_options(bet.children[1])))
    return bets    

async def main():
    base_url = "https://www.estorilsolcasinos.pt"
    browser = await uc.start()
    page = await browser.get(base_url + "/pt/apostas/proximos-eventos")  # sports betting page
    await page.maximize()
    time.sleep(0.8)
    sports = await get_all_sports(page)
    event_ids = []
    available_bets = []
    for sport in sports:
        await (await page.select(f'label[title="{sport}"]')).click()
        while True:
            try:
                await (await page.select('button.g1-button.secondary.negative', 0.5)).click()
            except Exception:
                break
        events_e = await page.select_all('div[id^="EventId"].bet-event-name.go-to-event.bet-event-name-col')
        ids = []
        [ids.append(event.parent.parent['id'].split('_')[-1]) for event in events_e]
        for id in ids:
            await (await page.select(f'div[id=EventId_{id}_EventName]')).click()
            time.sleep(0.5)
            available_bets.append(await get_all_bets(page))
            await page.back()
            time.sleep(0.5)
            try:
                await (await page.select(f'label[title="{sport}"]')).click()
            except Exception:
                pass
            print(available_bets)
        event_ids.append((sport, ids))

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
