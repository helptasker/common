import httpx

from helptasker_common.logger import cxt_request_id


async def test_app(client: httpx.AsyncClient):
    response = await client.get(url='/', headers={'Request-ID': '12345'})
    assert response.status_code == 200
    assert response.json().get('Hello') == 'World'
    assert response.headers.get('request-id') == '12345'


async def test_cxt_request_id(client: httpx.AsyncClient):
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


async def test_exception(client: httpx.AsyncClient):
    response = await client.get(url='/exception')
    assert response.status_code == 500


async def test_cors(client: httpx.AsyncClient):
    response = await client.options(
        url='/',
        headers={'Origin': 'http://localhost.local/', 'Access-Control-Request-Method': 'GET'},
    )
    assert response.headers.get('access-control-allow-methods') == 'GET'
    assert response.headers.get('access-control-max-age') == '300'


async def test_trusted(client: httpx.AsyncClient):
    response = await client.get(url='http://localhost2.local/')
    assert response.status_code == 400


async def test_healthcheck(client: httpx.AsyncClient):
    response = await client.get(url='http://localhost.local/healthcheck/')
    assert response.status_code == 200
