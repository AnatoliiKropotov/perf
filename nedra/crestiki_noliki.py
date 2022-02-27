
import numpy as np
import random

# функция, которая выполняет ходы игроков
def player(field, count):
    count += 1
    if count % 2 != 0:
        print(f"Ход №{count}, ходит игрок 1 \n")
        value = zero
    elif count % 2 == 0:
        value = crest
        print(f"Ход №{count}, ходит игрок 2 \n")
    else:
        print("Что-то пошло не так")
        exit()
    while True:
        number_row = random.randint(0, a - 1 )
        number_column = random.randint(0, b - 1)
        number = (number_row,number_column)
        if field[number] == 1:
            field[number] = value
            print(f"{field}\n")
            check_win(field, count)
            player(field, count)


# функция, которая проверяет условие победы
def check_win(field, count):
        # по столбцам
        column_sum = (np.sum(field, axis=0))
        for i in range(b):
            if column_sum[i] == 0:
                print(f"Победил игрок 1")
                exit()
            elif column_sum[i] == crest_check_column:
                print(f"Победил игрок 2")
                exit()

        # по строкам
        row_sum = (np.sum(field, axis=1))
        for i in range(a):
            if row_sum[i] == 0:
                print(f"Победил игрок 1")
                exit()
            elif row_sum[i] == crest_check_row:
                print(f"Победил игрок 2")
                exit()

        # проверка победы по диагонали запускается только для квадратных матриц
        if a == b:
            diagonal_1 = np.diagonal(field)
            diagonal_2 = np.fliplr(field).diagonal()

            if np.sum(diagonal_1) == 0 or np.sum(diagonal_2) == 0:
                print(f"Победил игрок 1")
                exit()
            elif np.sum(diagonal_1) == crest_check_column or np.sum(diagonal_2) == crest_check_column:
                print(f"Победил игрок 2")
                exit()

        # ничья после поледнего хода
        if count == max_hod:
            print("Ничья")
            exit()

        return


a = int(input("Введите количество строк:"))
b = int(input("Введите количество столбцов:"))
c = int(input("Введите количество подряд идущих символов для победы:"))
print(f"Задано игровое поле {a}x{b}")
print(f"Количество подряд идущих сиоволов {c}")
field = np.ones((a,b), dtype = np.int32)

zero = 0
# в качестве Х принимаем число 7
crest = 7
crest_check_column = 7 * a
crest_check_row = 7 * b
# максимальное количество ходов
max_hod= a * b
count = 0

print("----------------------------")
print("Игра началась")
player(field, count)
