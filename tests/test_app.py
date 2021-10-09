import pytest
import pytest_mock
import typecutter.app


######################################
# validate_args
######################################


def test_validate_args_both_files_not_exist(mocker: pytest_mock.MockerFixture):
    parser = typecutter.app.setup_argparser()
    args = parser.parse_args(args=["file.mp4", "-c", "file2.txt"])
    call_dict = {("file.mp4"): False, ("file2.txt"): False}

    error_spy = mocker.spy(parser, "error")

    with pytest.helpers.mock_with_call_dict(
        typecutter.app, "path_exists", call_dict
    ) as exists_mock:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            typecutter.app.validate_args(parser, args)

    assert exists_mock.call_count == 1
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

    error_spy.assert_called_once_with(f'Video file "file.mp4" does not exist.')


def test_validate_args_both_files_exist(mocker: pytest_mock.MockerFixture):
    parser = typecutter.app.setup_argparser()
    args = parser.parse_args(args=["file.mp4", "-c", "file2.txt"])
    call_dict = {"file.mp4": True, "file2.txt": True}

    error_spy = mocker.spy(parser, "error")

    with pytest.helpers.mock_with_call_dict(
        typecutter.app, "path_exists", call_dict
    ) as exists_mock:
        with pytest.helpers.does_not_raise():
            typecutter.app.validate_args(parser, args)

    assert exists_mock.call_count == 2
    assert error_spy.call_count == 0


def test_validate_args_cut_file_exists(mocker: pytest_mock.MockerFixture):
    parser = typecutter.app.setup_argparser()
    args = parser.parse_args(args=["file.mp4", "-c", "file2.txt"])
    call_dict = {("file.mp4"): False, ("file2.txt"): True}

    error_spy = mocker.spy(parser, "error")

    with pytest.helpers.mock_with_call_dict(
        typecutter.app, "path_exists", call_dict
    ) as exists_mock:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            typecutter.app.validate_args(parser, args)

    assert exists_mock.call_count == 1
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

    error_spy.assert_called_once_with(f'Video file "file.mp4" does not exist.')


def test_validate_args_video_file_exists(mocker: pytest_mock.MockerFixture):
    parser = typecutter.app.setup_argparser()
    args = parser.parse_args(args=["file.mp4", "-c", "file2.txt"])
    call_dict = {("file.mp4"): True, ("file2.txt"): False}

    error_spy = mocker.spy(parser, "error")

    with pytest.helpers.mock_with_call_dict(
        typecutter.app, "path_exists", call_dict
    ) as exists_mock:
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            typecutter.app.validate_args(parser, args)

    assert exists_mock.call_count == 2
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

    error_spy.assert_called_once_with(f'Cut file "file2.txt" does not exist.')


######################################
# run
######################################

# TODO


######################################
# main_with_args
######################################

# TODO
