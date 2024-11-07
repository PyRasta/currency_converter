import asyncpg

from config import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DATABASE


async def connect_to_database():
    connection = await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DATABASE,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    return connection


class Db:
    def __init__(self, connection):
        self.connection = connection

    async def send_request_db_write(self, query: str, params: tuple = ()):
        response = {'status': bool, 'message': str}
        try:
            async with self.connection.transaction():
                if params:
                    await self.connection.execute(query, *params)
                else:
                    await self.connection.execute(query)
                response['status'] = True
                return response
        except Exception as error:
            response['status'] = False
            response['message'] = error
        finally:
            return response

    async def send_request_db_read(self, query: str, params: tuple = ()):
        response = {'status': bool, 'message': str}
        try:
            async with self.connection.transaction():
                if params:
                    result = await self.connection.fetch(query, *params)
                else:
                    result = await self.connection.fetch(query)
                response['status'] = True
                response['message'] = result
                return response
        except Exception as error:
            response['status'] = False
            response['message'] = error
        finally:
            return response

    async def add_symbol_rate(self, symbol: str, rate: float):
        query = 'INSERT INTO symbols_rate (symbol, rate) VALUES ($1, $2);'
        params = (symbol, rate,)
        response = await self.send_request_db_write(query, params)
        return response

    async def update_symbol_rate(self, symbol: str, rate: float):
        query = 'UPDATE symbols_rate SET rate = $1 WHERE symbol = $2'
        params = (rate, symbol,)
        response = await self.send_request_db_write(query, params)
        return response

    async def get_symbol_rate(self, symbol: str):
        query = 'SELECT rate FROM symbols_rate WHERE symbol = $1'
        params = (symbol,)
        response = await self.send_request_db_read(query, params)
        return response

    async def get_all_symbol(self):
        query = 'SELECT symbol FROM symbols_rate'
        response = await self.send_request_db_read(query)
        symbols = []
        if response['status']:
            for symbol in response['message']:
                symbols.append(symbol['symbol'])
            return {'status': True, 'message': symbols}
        return response
