from pydantic import ValidationError

import pytest

from ufaas.tasks import FnTask

from .task_fixtures import VALID_TASK_BASIC


@pytest.mark.asyncio
async def test_task_validity() -> None:
    """
    Given a valid task spec, does task successfully validate?
    Also, does a spec of gibberish/invalid types successfully error?
    """
    FnTask(**VALID_TASK_BASIC)
    with pytest.raises(TypeError) as e_info:  # noqa F841
        FnTask(**{"foo": "bar"})


@pytest.mark.asyncio
async def test_task_type_validation() -> None:
    """
    Test task type validation works.
    """
    # Should error on `name` being too long. If error, success.
    name_too_long = VALID_TASK_BASIC
    name_too_long["task_name"] = "C" * 500  # 500 'C' chars. Limit 127.
    with pytest.raises(ValidationError) as e_info: # noqa F841
        FnTask(**name_too_long)


@pytest.mark.asyncio
async def test_task_validator_method() -> None:
    """
    Test task validation / coercion methods.
    """
    # test name has spaces replaced with underscores.
    name_with_spaces = VALID_TASK_BASIC
    name_with_spaces["task_name"] = "foo bar"
    assert "foo_bar" == FnTask(**name_with_spaces).task_name
