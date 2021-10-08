from typing import Match

import pytest
import typecutter.parser as parser
from typecutter.common import Cut

######################################
# validate_match
######################################


def test_validate_match_ok():
    test_match: Match[str] = parser.cuts_regex.match(
        f"{parser.cuts_prefix}1, 2 a # 1234"
    )
    with pytest.warns(None) as records:
        parser.validate_match(test_match)
    pass


def test_validate_match_warning_precomment():
    test_match: Match[str] = parser.cuts_regex.match(
        f"{parser.cuts_prefix}1, 2 a b # 1234"
    )
    with pytest.warns(UserWarning) as records:
        parser.validate_match(test_match)

    assert len(records) == 1
    assert (
        str(records[0].message)
        == 'Cut name should contain no spaces. "a" would be used as the cut name.'
    )


######################################
# validate_cut
######################################


def test_validate_cut_ok():
    test_cut = Cut(1, 2, None)
    with pytest.warns(None) as records:
        parser.validate_cut(test_cut)
    assert len(records) == 0


def test_validate_cut_start_end():
    test_cut = Cut(5678, 1234, None)
    with pytest.raises(ValueError) as exception_info:
        parser.validate_cut(test_cut)

    assert exception_info is not None
    assert exception_info.type == ValueError
    assert (
        exception_info.value.args[0]
        == 'Start frame "5678" must be smaller-equals to end frame "1234".'
    )


def test_validate_cut_nonascii_name_hebrew():
    test_cut = Cut(1234, 5678, "חיתוך")
    with pytest.raises(ValueError) as exception_info:
        parser.validate_cut(test_cut)

    assert exception_info is not None
    assert exception_info.type == ValueError
    assert exception_info.value.args[0] == 'Cut name "חיתוך" must be in ASCII.'


def test_validate_cut_nonascii_name_japanese():
    test_cut = Cut(1234, 5678, "カット")
    with pytest.raises(ValueError) as exception_info:
        parser.validate_cut(test_cut)

    assert exception_info is not None
    assert exception_info.type == ValueError
    assert exception_info.value.args[0] == 'Cut name "カット" must be in ASCII.'


def test_validate_cut_both_raises_first():
    test_cut = Cut(5678, 1234, None)
    with pytest.raises(ValueError) as exception_info:
        parser.validate_cut(test_cut)

    assert exception_info is not None
    assert exception_info.type == ValueError
    assert (
        exception_info.value.args[0]
        == 'Start frame "5678" must be smaller-equals to end frame "1234".'
    )


######################################
# parse_cut
######################################


def test_parse_cut_simple():
    input_str = f"{parser.cuts_prefix}1,2"
    test_match: Match[str] = parser.cuts_regex.match(input_str)
    output = parser.parse_cut(test_match)
    assert output == Cut(1, 2, None)


def test_parse_cut_with_space():
    input_str = f"{parser.cuts_prefix}1, 2"
    test_match: Match[str] = parser.cuts_regex.match(input_str)
    output = parser.parse_cut(test_match)
    assert output == Cut(1, 2, None)


def test_parse_cut_with_space_comments():
    input_str = f"{parser.cuts_prefix}1, 2 # Comment here"
    test_match: Match[str] = parser.cuts_regex.match(input_str)
    output = parser.parse_cut(test_match)
    assert output == Cut(1, 2, None)


def test_parse_cut_with_space_name():
    input_str = f"{parser.cuts_prefix}1, 2 Stuff"
    test_match: Match[str] = parser.cuts_regex.match(input_str)
    output = parser.parse_cut(test_match)
    assert output == Cut(1, 2, "Stuff")


def test_parse_cut_with_space_name_comment():
    input_str = f"{parser.cuts_prefix}1, 2 Stuff # comment"
    test_match: Match[str] = parser.cuts_regex.match(input_str)
    output = parser.parse_cut(test_match)
    assert output == Cut(1, 2, "Stuff")


######################################
# parse_typecuts
######################################


def test_parse_typecuts_single():
    input_str = f"{parser.cuts_prefix}1,2"
    output = parser.parse_typecuts(input_str)
    assert output == [Cut(1, 2, None)]


def test_parse_typecuts_single_with_space():
    input_str = f"{parser.cuts_prefix}1, 2"
    output = parser.parse_typecuts(input_str)
    assert output == [Cut(1, 2, None)]


def test_parse_typecuts_single_with_space_comments():
    input_str = f"{parser.cuts_prefix}1, 2 # Comment here"
    output = parser.parse_typecuts(input_str)
    assert output == [Cut(1, 2, None)]


def test_parse_typecuts_single_with_space_name():
    input_str = f"{parser.cuts_prefix}1, 2 Stuff"
    output = parser.parse_typecuts(input_str)
    assert output == [Cut(1, 2, "Stuff")]


def test_parse_typecuts_single_with_space_name_comment():
    input_str = f"{parser.cuts_prefix}1, 2 Stuff # comment"
    output = parser.parse_typecuts(input_str)
    assert output == [Cut(1, 2, "Stuff")]


def test_parse_typecuts_single_with_space_name_precomment():
    input_str = f"{parser.cuts_prefix}1, 2 Stuff With Spaces"
    with pytest.warns(UserWarning) as records:
        output = parser.parse_typecuts(input_str)

    assert len(records) == 1
    assert (
        str(records[0].message)
        == 'Cut name should contain no spaces. "Stuff" would be used as the cut name.'
    )
    assert output == [Cut(1, 2, "Stuff")]


def test_parse_typecuts_single_with_space_name_precomment_comment():
    input_str = f"{parser.cuts_prefix}1, 2 Stuff With Spaces # A witty comment"
    with pytest.warns(UserWarning) as records:
        output = parser.parse_typecuts(input_str)

    assert len(records) == 1
    assert (
        str(records[0].message)
        == 'Cut name should contain no spaces. "Stuff" would be used as the cut name.'
    )
    assert output == [Cut(1, 2, "Stuff")]


def test_parse_typecuts_single_with_data():
    input_str = f"""
{parser.cuts_prefix}1,2
this is some data
    """.strip()
    output = parser.parse_typecuts(input_str)
    assert output == [Cut(1, 2, None)]


def test_parse_typecuts_multiple():
    input_str = f"""
{parser.cuts_prefix}1,2
{parser.cuts_prefix}3,4
{parser.cuts_prefix}5,6
    """.strip()
    output = parser.parse_typecuts(input_str)
    assert output == [
        Cut(1, 2, None),
        Cut(3, 4, None),
        Cut(5, 6, None),
    ]


def test_parse_typecuts_multiple_various_styles():
    input_str = f"""
{parser.cuts_prefix}1, 2
{parser.cuts_prefix}3,4
{parser.cuts_prefix}5, 6
    """.strip()
    output = parser.parse_typecuts(input_str)
    assert output == [
        Cut(1, 2, None),
        Cut(3, 4, None),
        Cut(5, 6, None),
    ]


def test_parse_typecuts_names():
    input_str = f"""
{parser.cuts_prefix}1,2 Aei
{parser.cuts_prefix}3,4 Bee
{parser.cuts_prefix}5,6 Ci
    """.strip()
    output = parser.parse_typecuts(input_str)
    assert output == [
        Cut(1, 2, "Aei"),
        Cut(3, 4, "Bee"),
        Cut(5, 6, "Ci"),
    ]


def test_parse_typecuts_mutiple_various_styles_various_data():
    input_str = f"""
{parser.cuts_prefix}1, 2
this is with data

{parser.cuts_prefix}3,4
some good old 日本語 here.

{parser.cuts_prefix}5, 6
מידע בעברית
    """.strip()
    output = parser.parse_typecuts(input_str)
    assert output == [
        Cut(1, 2, None),
        Cut(3, 4, None),
        Cut(5, 6, None),
    ]


def test_parse_typecuts_real_example():
    input_str = f"""
:24, 84
:85, 179
00:00 - 00:08
多須小学校入学式
טקס כניסה לבית הספר היסודי

:384, 500
00:16 - 00:21
多須小学校入学式
טקס כניסה לבית הספר היסודי

:572, 626
00:24 - 00:26
多須小学校入学式
טקס כניסה לבית הספר היסודי

:993, 1087
00:42 - 00:46
多須小学校入学式
טקס כניסה לבית הספר היסודי

:1177, 1319
00:49 - 00:55
多須小学校入学式
טקס כניסה לבית הספר היסודי

:11658, 11752
08:06 - 08:11
つたわることば
מילים מספרות

しょうがくこくご
לשון לבית הספר היסודי

たのしいさんすう
חשבון בכיף

:22586,22675
15:42-15:45
家
בית

大きい木
עץ גדול

ここ
כאן

:23011,23203
כנ"ל
    """.strip()
    output = parser.parse_typecuts(input_str)
    assert output == [
        Cut(24, 84, None),
        Cut(85, 179, None),
        Cut(384, 500, None),
        Cut(572, 626, None),
        Cut(993, 1087, None),
        Cut(1177, 1319, None),
        Cut(11658, 11752, None),
        Cut(22586, 22675, None),
        Cut(23011, 23203, None),
    ]
