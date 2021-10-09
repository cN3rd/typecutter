import pytest


def test_mock_with_call_single():
    class A:
        def a(self, b):
            return b

    ainst = A()

    with pytest.helpers.mock_with_call_dict(ainst, "a", call_dict={(1): 5, (3): 6}):
        assert ainst.a(1) == 5
        assert ainst.a(3) == 6
        assert ainst.a(2) == 2


def test_mock_with_call_dict_multiple():
    class A:
        def a(self, b, c):
            return b + c

    ainst = A()

    with pytest.helpers.mock_with_call_dict(
        ainst, "a", call_dict={(1, 2): 5, (3, 4): 6}
    ):
        assert ainst.a(1, 2) == 5
        assert ainst.a(3, 4) == 6
        assert ainst.a(1, 1) == 2


def test_change_working_directory():
    import pathlib
    import tempfile

    get_cwd = lambda: pathlib.Path(".").resolve()

    old_cwd = get_cwd()
    with tempfile.TemporaryDirectory() as tempdir:
        with pytest.helpers.change_working_directory(tempdir):
            assert get_cwd() != old_cwd
    assert get_cwd() == old_cwd
