import asyncio

from db import connect_to_database, Db


class Converter:
    def __init__(self, symbol_from: str, symbol_to: str, value: float):
        self.symbol_from = symbol_from.upper()
        self.symbol_to = symbol_to.upper()
        self.value = value

    async def get_rate(self):
        connection = await connect_to_database()
        db = Db(connection)
        symbols = await db.get_all_symbol()
        if symbols['status']:
            if self.symbol_from not in symbols['message']:
                return {'status': False, 'message': f'Not found {self.symbol_from}'}
            elif self.symbol_to not in symbols['message']:
                return {'status': False, 'message': f'Not found {self.symbol_to}'}
            else:
                rate_usd_from = await db.get_symbol_rate(self.symbol_from)
                rate_usd_to = await db.get_symbol_rate(self.symbol_to)
                if rate_usd_from['status'] and rate_usd_to['status']:
                    rate_usd_from = rate_usd_from['message'][0]['rate']
                    rate_usd_to = rate_usd_to['message'][0]['rate']
                    rate_from_usd = 1 / rate_usd_from
                    rate = rate_from_usd * rate_usd_to
                    result = round(rate * self.value, 2)
                    return {'status': True, 'message': result}
                else:
                    return {'status': False, 'message': 'Not get rate'}
        else:
            return {'status': False, 'message': 'Not get all symbols in database'}
