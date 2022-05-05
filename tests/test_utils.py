from handlers import show_last_5
from utils import get_from_googlesheet, get_last_5_records


def test_length_of_list_from_googlesheet():
    sheet = get_from_googlesheet()
    values = get_last_5_records(sheet)
    assert len(values) == 5
    assert len(values[-1]) == 2
    assert isinstance(values[-1][0], str)
    assert isinstance(values[-1][1], int)


# def test_allowed_user_dec():
#     assert show_last_5() == ''
