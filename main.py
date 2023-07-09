""" Модуль реализации виджета 'Операции по счетам' клиента
    На входе: запакованный  в zip-архиве файл с операциями клиента
    На выходе: вывод на экран 5-ти последних успешных транзакций """

from pyunpack import Archive
import pathlib

import func



if __name__ == '__main__':
    actions_source = pathlib.Path.cwd()/ 'src'/'operations.zip'
    # распакуем файл из архива (источник может и передаваться на вход в виде zip-файла)
    Archive(actions_source).extractall(pathlib.Path.cwd())
    last_five_transactions = func.last5_actions(func.read_actions(func.transactions_file))
    print(func.chain_last_transactions(last_five_transactions))
