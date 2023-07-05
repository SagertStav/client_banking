""" Тесты для виджета transactions """
import pytest, main


def test_read_actions():
    all_transactions = main.read_actions('src\operations.json')
    print(len(all_transactions))
    assert len(all_transactions) == 101  #по предложенному источнику для курсовой




test_read_actions
