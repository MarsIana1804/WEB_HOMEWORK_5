import aiohttp
import asyncio
import sys
from datetime import datetime, timedelta

async def fetch_exchange_rates(days, currencies):
    url = "https://api.privatbank.ua/p24api/exchange_rates?json&date={}"
    exchange_rates = []

    async with aiohttp.ClientSession() as session:
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%d.%m.%Y")
            async with session.get(url.format(date)) as response:
                data = await response.json()
                rates_for_date = {date: {}}
                #print(data)
                for rate in data.get("exchangeRate", []):
                    if rate['currency'] in currencies:
                        currency = rate['currency']
                        rates_for_date[date][currency] = {
                            "sale": rate["saleRate"],
                            "purchase": rate["purchaseRate"]
                        }
                
                exchange_rates.append(rates_for_date)
    return exchange_rates

async def main(days, currencies):
    exchange_rates = await fetch_exchange_rates(days, currencies)
    print(exchange_rates)

if __name__ == "__main__":
    try:
        days = int(sys.argv[1])
        currencies = sys.argv[2:] if len(sys.argv) > 2 else ['EUR', 'USD']
        if "UAH" in currencies:
            print("Error: You can't check this currency' rate.")
            sys.exit(1)

        print(currencies)
        
        if days > 10:
            print("Error: Number of days should not exceed 10.")
            sys.exit(1)
    except (ValueError, IndexError):
        print("Usage: python main.py <number_of_days> [<currency1> <currency2> ...]")
        sys.exit(1)

    asyncio.run(main(days, currencies))

