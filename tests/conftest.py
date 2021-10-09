import contextlib
import os
import pathlib
import unittest.mock as mock
from typing import Any, ContextManager

import pytest

pytest_plugins = ["helpers_namespace"]


@pytest.helpers.register
@contextlib.contextmanager
def mock_with_call_dict(
    target: Any, attribute: str, call_dict: dict[Any, Any]
) -> ContextManager:
    fallback = getattr(target, attribute)
    call_dict = {(k,) if type(k) is not tuple else k: v for k, v in call_dict.items()}

    with mock.patch.object(target, attribute) as mock_cm:

        def _call(*args, **kwargs):
            call_args = (*args, *kwargs)
            return call_dict.get(call_args, fallback(*call_args))

        mock_cm.side_effect = _call
        yield mock_cm


@pytest.helpers.register
@contextlib.contextmanager
def does_not_raise():
    yield


@pytest.helpers.register
@contextlib.contextmanager
def change_working_directory(newdir: pathlib.Path):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
