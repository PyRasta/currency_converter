import asyncio
import aiohttp
from celery import Celery

from db import Db, connect_to_database
from config import ACCESS_KEY, REDIS_URL, REDIS_URL_RESULT_BACKEND, TIME_UPDATE_RATES_SEC

celery = Celery('tasks', broker=REDIS_URL, result_backend=REDIS_URL_RESULT_BACKEND)
celery.conf.beat_schedule = {
    'my-periodic-task': {
        'task': 'rate.run',
        'schedule': TIME_UPDATE_RATES_SEC
    },
}


async def get_all_currency(access_key: str):
    url = f'http://api.currencylayer.com/live?access_key={access_key}&format=1'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.json()
            if response['success']:
                return response
            return False


async def update_rate_all_symbol():
    connection = await connect_to_database()
    db = Db(connection)
    currency = await get_all_currency(ACCESS_KEY)
    symbols = await db.get_all_symbol()
    if currency:
        if symbols['status']:
            for symbol, rate in currency['quotes'].items():
                symbol = symbol.replace('USD', '')
                if symbol not in symbols['message']:
                    await db.add_symbol_rate(symbol, rate)
                else:
                    await db.update_symbol_rate(symbol, rate)
    await connection.close()


@celery.task
def run():
    asyncio.run(update_rate_all_symbol())
