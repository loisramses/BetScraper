# i have to simulate the post and options request, still studying how to do it

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

async def main():
    global page
    global request_options
    browser = await zd.start()
    page = await browser.get('https://apostas.goldenpark.pt/')

    request_options = {
        'method': 'POST',
        'headers': {
          'Accept-Language': 'pt-PT',
          'Content-type': 'charset=UTF-8',
        },
        'body': json.dumps({
            "context":{
                "url_key":"/desporte/13-futebol",
                "device":"web_vuejs_desktop"
            }
        })
    }
    
    await browser.wait(10)
    result = await request_data('https://ws.goldenpark.pt/component/datatree', request_options)
    await browser.wait(30)
    print(result)
    # with open('./src/lebull/data.json', 'w', encoding='utf-8') as file:
    #     json.dump(result, file, ensure_ascii=False, indent=2)
        
    await browser.stop()

if __name__ == "__main__":
    zd.loop().run_until_complete(main())
