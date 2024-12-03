import nodriver as uc
import time  # Importando a biblioteca time para medir o tempo

# url for the games is https://www.estorilsolcasinos.pt/pt/apostas/event/{sportId}/0/{leagueId}/matchId

async def main():
    base_url = "https://www.estorilsolcasinos.pt"
    browser = await uc.start()
    page = await browser.get(base_url + "/pt/apostas")  # sports betting page

    await (
        await page.select('a[data-bind*="$root.moreLessSport"]')
    ).click()  # click the "mais desportos" on the left menu

    sports_e = await page.select_all(
        'a[href*="/pt/apostas/desporto/"'
    )  # find all sports links

    # for url, open a new tab
    competitions = []
    for sport_e in sports_e:
        print(f"{sport_e.text}: {sport_e.attrs['href']}")
        tab = await browser.get(base_url + sport_e.attrs["href"])
        competitions_e = await tab.select_all(
            'div.aside__container a[data-bind*="league.name"]'
        )

        for competition_e in competitions_e:
            competitions.append(
                (
                    competition_e.attrs['href'],
                    competition_e.text.split(' - ')[-1].strip(),
                )
            )
    print(f'size: {len(competitions)}, {competitions}')


if __name__ == "__main__":
    start_time = time.time()  # Marcar o tempo de início
    uc.loop().run_until_complete(main())
    end_time = time.time()  # Marcar o tempo de término
    print(f'Tempo total de execução: {end_time - start_time:.2f} segundos')
