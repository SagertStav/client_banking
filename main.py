""" Модуль реализации виджета 'Операции по счетам' клиента
    На входе: запакованный  в zip-архиве файл с операциями клиента
    На выходе: вывод на экран 5-ти последних успешных транзакций """

from pyunpack import Archive
import pathlib
from pathlib import Path
import json

transactions_file = Path(pathlib.Path.cwd(), '', '', 'src\operations.json')


def read_actions(transactions_json_file):
    ''' read_actions() считывает в память из json-файла транзакции клиента,
     возвращая объект - загруженный список словарей с операциями по счетам/картам клиента '''
    try:
        with open(transactions_json_file, 'r', encoding='utf-8') as f:  # открыли файл с данными
            # для run                               проходит низлежащий путь src\operations.json,
            # а для тестов в терминале (poetry run pytest --cov) - только ..\src\operations.json  с двумя точками

            return json.load(f)  # загнали все, что получилось в переменную
    except FileNotFoundError:
        with open(Path(pathlib.Path.cwd(), '', '', '..\src\operations.json'), 'r',
                  encoding='utf-8') as f:  # открыли файл с данными
            return json.load(f)  # загнали все, что получилось в переменную


def last5_actions(client_transactions):
    ''' Функция last5_actions() выбирает последние 5 УСПЕШНЫХ транзакций клиента,
   возвращая отсортированный по убыванию дат операций список
   :param client_transactions: - список словарей - всех транзакций клиента
   :return: - выборка только 5-ти последних состоявшихся операций (список) '''

    return sorted([x for x in client_transactions \
                   if x.get('state') == "EXECUTED"], reverse=True, \
                  key=lambda k: k['date'])[:5]  # топ 5-ти первых уже отсортированных по убыванию


def my_dd_mm_yyyy_format(datetime_str):
    ''' Функция, возвращающая из текстовой строку
    (по формату внешнего источника-архива с операциями клиента)
    с датой/временем операций - ДАТУ в формате ДД.ММ.ГГГГ '''

    yyyy, mm, dd = datetime_str[:10].split('-')  # использую распаковку сразу в 3 переменные (год, месяц, день)
    return f"{dd}.{mm}.{yyyy}"


def masked_account(account_str):
    ''' masked_account() маскирует полный вывод номера счета или карты
   Для счета **XXXX - только последние 4 цифры.
   Для карты XXXX XX** **** XXXX - видны первые 6 цифр и последние 4,
   с пробелами между блоками по 4 цифры '''

    return '' if account_str is None \
        else ("счет **" + account_str[-4:]) if 'счет' == account_str[:4].lower() \
        else account_str[:-14] + "** **** " + account_str[-4:]


def chain_last_transactions(last_transactions, n=5):
    ''' show_last_transactions() выводит на экран по умолчанию последние 5 состоявшихся транзакций:
    дату, сумму, валюту операции, краткое описание, id операции, на какой счет и с какого (при наличии),
    разделенные пустой строкой '''

    print(last_transactions)
    return "\n\n".join([f"{my_dd_mm_yyyy_format(last_transactions[i].get('date'))} сумма " +
                        format(last_transactions[i].get('operationAmount')['amount'], " >12") + " " +
                        format(last_transactions[i].get('operationAmount')['currency']['name'], " <4") +
                        "- " + format(last_transactions[i].get('description'), " <25") +
                        "№ оп." + format(last_transactions[i].get('id'), " >12") + ": " +
                        f"{masked_account(last_transactions[i].get('to'))} " + \
                        (("<= " + format(masked_account(last_transactions[i].get('from')), " >27")) \
                             if 'from' in list(last_transactions[i].keys()) else '') for i in
                        range(0, min(n, len(last_transactions)))])


if __name__ == '__main__':
    actions_source = Path(pathlib.Path.cwd(), '', '', 'src\operations.zip')
    # распакуем файл из архива (источник может и передаваться на вход в виде zip-файла)
    Archive(actions_source).extractall(pathlib.Path.cwd())
    last_five_transactions = last5_actions(read_actions(transactions_file))
    # print(last_five_transactions)
    print(chain_last_transactions(last_five_transactions))
