import aiohttp, asyncio,datetime,json,sys

async def fetch_exchange_rate(session, date):
    async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') as response:
        result = await response.json()
        return date, result

async def main_func(x:int):
    if x <= 10:
        today = datetime.date.today()
        dates = [today - datetime.timedelta(days=i) for i in range(x)]
        async with aiohttp.ClientSession() as session:
            tasks = [fetch_exchange_rate(session, date) for date in dates]
            results = await asyncio.gather(*tasks)
            cleaned_results = {date: clean_data(data) for date, data in results}
            return cleaned_results
        
    else:
        print("A maximum 10 days")
        sys.exit(1)

def clean_data(data):
    for item in data:
        if item['base_ccy']:
            del item['base_ccy']

    return data

if __name__ == "__main__":
    if len(sys.argv) > 2:
        sys.exit(1)
    try:
        x = int(sys.argv[1])
    except Exception:
        sys.exit(1)
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main_func(x))
    for date, data in results.items():
        print(date,json.dumps(data, indent=2))
   