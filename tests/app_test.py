import httpx

from helptasker_common.logger import cxt_request_id


async def test_app(client: httpx.AsyncClient, caplog):
    response = await client.get(url='/', headers={'Request-ID': '12345'})
    assert response.status_code == 200
    assert response.json().get('Hello') == 'World'
    assert response.headers.get('request-id') == '12345'


async def test_cxt_request_id(client: httpx.AsyncClient, caplog):
    cxt_request_id.set('12345')
    response = await client.get(url='/?test=1')
    assert response.status_code == 200


async def test_cxt_api_v1(client: httpx.AsyncClient):
    response = await client.get(url='/api/v1/test')
    assert response.status_code == 200
    assert response.json().get('api_version') == 1


async def test_cxt_api_v2(client: httpx.AsyncClient):
    response = await client.get(url='/api/v2/test')
    assert response.status_code == 200
    assert response.json().get('api_version') == 2
