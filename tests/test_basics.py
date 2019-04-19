from lessl.lessl import app as myapp

import pytest

from quart import Quart


@pytest.fixture
def app() -> Quart:
    return myapp


@pytest.mark.asyncio
async def test_index(app: Quart) -> None:
    """Test if the index at the route is working (webserver and routes up)."""
    test_client = app.test_client()
    response = await test_client.get('/')
    assert response.status_code == 200
