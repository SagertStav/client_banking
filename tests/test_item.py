""" Тесты для виджета transactions """
import pytest, main, pathlib
import func


def test_read_actions():
    #all_transactions = main.read_actions('src\operations.json')
    all_transactions = func.read_actions(func.transactions_file)
    print(len(all_transactions))
    assert len(all_transactions) == 101  #по предложенному источнику для курсовой

def test_my_dd_mm_yyyy_format():
    assert func.my_dd_mm_yyyy_format("2019-08-26T10:50:58.294041") == "26.08.2019"

def test_masked_account():
    assert func.masked_account("Счет 64686473678894779589") == "счет **9589"

def test_chain_last_transactions():
 #   print(main.chain_last_transactions(main.last5_actions(main.read_actions('src\operations.json')),2))
    s=func.read_actions(func.transactions_file)
    s2=func.last5_actions(s)
    print('s2:', s2)


    print(func.chain_last_transactions(s2, 1))
    assert func.chain_last_transactions(s2,1) == "08.12.2019 сумма     41096.24 USD - Открытие вклада          № оп.   863064926: счет **5907"

def test_last5_actions():
    s=func.read_actions(func.transactions_file)
    s2 = func.last5_actions(s)
    assert [float(x.get('operationAmount')['amount']) for x in s2] == [41096.24, 48150.39, 30153.72, 62814.53, 21344.35]



"""
"08.12.2019 сумма     41096.24 USD - Открытие вклада          № оп.   863064926: счет **5907

07.12.2019 сумма     48150.39 USD - Перевод организации      № оп.   114832369: счет **3655 <= Visa Classic 28** **** 9012"
"""

print('Теытф: ',f"{(pathlib.Path.cwd().parent if pathlib.Path.cwd().name[-5:]=='tests' else pathlib.Path.cwd()) / 'src'/'operations.json'}")

test_read_actions()
test_my_dd_mm_yyyy_format()
test_masked_account()



test_chain_last_transactions()


test_last5_actions()