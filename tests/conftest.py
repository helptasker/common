from typing import AsyncGenerator

import fastapi
import httpx
import pytest
from fastapi import FastAPI

from helptasker_common import middlewares
from helptasker_common.http_base_client import http_base_client
from helptasker_common.instrumentation import HelpTaskerCommonFastApiInstrumentator
from helptasker_common.logger import logger_init

app = FastAPI()

HelpTaskerCommonFastApiInstrumentator(
    cors_enable=True,
    trusted_host_enable=True,
    trusted_host_allowed_hosts=['localhost.local'],
).instrument(app)


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@app.get('/api/v1/test')
def api_v1():
    return {'api_version': 1}


@app.get('/api/v2/test')
def api_v2():
    return {'api_version': 2}


@app.get('/exception')
def exception():
    raise Exception('test')


@pytest.fixture()
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    headers = {'x-real-ip': '127.0.0.1'}
    async with http_base_client(app=app, base_url='http://localhost.local', headers=headers) as client:
        yield client
        await client.aclose()
