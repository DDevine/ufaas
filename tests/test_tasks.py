from pydantic import ValidationError

import pytest

from quart import Quart

from ufaas.ufaas import Task
from ufaas.ufaas import app as myapp

from .task_fixtures import (INVALID_TASK_BASIC, INVALID_TASK_NAME_TOO_LONG,
                            VALID_TASK_BASIC)


@pytest.fixture
def app() -> Quart:
    return myapp


@pytest.mark.asyncio
async def test_parse_task_invalid() -> None:
    """
    Test that given an INVALID task creation fails.
    """
    # with pytest.raises(Exception) as e_info:
    return


@pytest.mark.asyncio
async def test_task_validity() -> None:
    """
    Given a valid task spec, does task successfully validate?
    Also, does a spec of gibberish/invalid types successfully error?
    """
    Task(**VALID_TASK_BASIC)
    with pytest.raises(TypeError) as e_info:  # noqa F841
        Task(**INVALID_TASK_BASIC)


@pytest.mark.asyncio
async def test_task_name_too_long() -> None:
    """
    Test task validation for name length works.
    """
    with pytest.raises(ValidationError) as e_info: # noqa F841
        Task(**INVALID_TASK_NAME_TOO_LONG)


@pytest.mark.asyncio
async def test_create_task() -> None:
    """
    Test that a task can be created.
    """
    return
