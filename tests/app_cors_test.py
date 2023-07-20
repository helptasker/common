import httpx


async def test_cors(client: httpx.AsyncClient, caplog):
    response = await client.options(
        url='/',
        headers={'Origin': 'http://localhost.local/', 'Access-Control-Request-Method': 'GET'},
    )
    assert response.headers.get('access-control-allow-methods') == 'GET'
