import json

from ufaas.ufaas import app as myapp

import pytest

from quart import Quart

from .tasks import VALID_BASIC_INLINE_TASK_SPEC


@pytest.fixture
def app() -> Quart:
    return myapp


@pytest.mark.asyncio
async def test_parse_task_valid() -> None:
    """
    Test that given a VALID task creation succeeds.
    """
    # Check that entities can be encoded to JSON.
    assert json.dumps(VALID_BASIC_INLINE_TASK_SPEC)
    return


@pytest.mark.asyncio
async def test_parse_task_invalid() -> None:
    """
    Test that given an INVALID task creation fails.
    """
    # with pytest.raises(Exception) as e_info:
    return


@pytest.mark.asyncio
async def test_create_task() -> None:
    """
    Test that a task can be created.
    """
    return
