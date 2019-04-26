import pytest

from quart import Quart

from ufaas.ufaas import app as myapp

from .task_fixtures import VALID_TASK_BASIC


@pytest.fixture
def app() -> Quart:
    # TODO: mock Docker API so that docker tests work.
    return myapp


@pytest.mark.asyncio
async def test_index(app: Quart) -> None:
    """Test if the index works."""
    test_client = app.test_client()
    response = await test_client.get('/')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_fn_create(app: Quart) -> None:
    """
    Test POST /fn/ for task creation.
    """
    test_client = app.test_client()
    response = await test_client.post(
        "/fn", json=VALID_TASK_BASIC
    )
    assert response.status_code == 200
    response_json = await response.get_json()
    assert response_json == VALID_TASK_BASIC
