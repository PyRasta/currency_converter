import asyncio

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, constr

from converter import Converter


app = FastAPI()


class Params(BaseModel):
    from_: constr(to_upper=True, max_length=3)
    to: constr(to_upper=True, max_length=3)
    value: float


@app.get('/api/rates')
async def get_rate(from_: constr(to_upper=True, max_length=3), to: constr(to_upper=True, max_length=3), value: float):
    converter = Converter(from_, to, value)
    result = await converter.get_rate()
    response = {'result': result['message']}
    if result['status']:
        return JSONResponse(response, status_code=200)
    else:
        return JSONResponse(response, status_code=400)