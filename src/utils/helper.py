import zendriver

async def request_data(fetch_url: str, request_options: dict, page: zendriver.Tab) -> dict:
    script = f"""
    fetch('{fetch_url}', {request_options}).then(response => response.json()).catch((error) => console.error(error))
    """
    return await page.evaluate(script, await_promise=True)
