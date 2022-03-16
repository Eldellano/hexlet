from functions import get_function

get = get_function()

if get({'a': 1, 'b': 2, 'c': 3}, 'b') != 2:
    raise Exception('Функция работает неверно!')

if get({'a': 1, 'b': 2, 'c': 3}, 'k', 'def') != 'def':
    raise Exception('Функция работает неверно!')

if get({'a': 1, 'b': 2, 'c': 3}, 'b', 'b') != 2:
    raise Exception('Функция работает неверно!')

print('Все тесты пройдены!')
