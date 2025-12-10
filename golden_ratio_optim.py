import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

# Начальный интервал поиска и точность
a0 = -10
b0 = 30
eps = 0.000001


def f(x):
    # Тестовая целевая функция
    return 1 - x**2


def negative_f(x):
    # Функция с противоположным знаком (если экстремум максимум)
    return -(1 - x**2)


def type_of_extremum(a_, b_, f_):
    c = (a_ + b_) / 2
    if f_(a_) > f_(c) or f_(b_) > f_(c):
        type_ex = 'минимум'
    else:
        type_ex = 'максимум'
    return type_ex


def golden_ratio(a_, b_, f_, eps_):
    ak, bk, x_list = [], [], []

    left = a_
    right = b_
    t = (3 - np.sqrt(5)) / 2
    print(t)

    ak.append(left)
    bk.append(right)
    x = (left + right) / 2
    x_list.append(x)

    x1 = left + (right - left) * t
    x2 = right - (right - left) * t
    f1 = f_(x1)
    f2 = f_(x2)

    while abs(left - right) > eps_:
        if f1 < f2:
            right = x2
            x2 = x1
            f2 = f1
            x1 = left + (right - left) * t
            f1 = f_(x1)
        else:
            left = x1
            x1 = x2
            f1 = f2
            x2 = right - (right - left) * t
            f2 = f_(x2)

        ak.append(left)
        bk.append(right)
        x = (left + right) / 2
        x_list.append(x)

    return ak, bk, x_list


type_ex = type_of_extremum(a0, b0, f)
print('Тип экстремума: ' + type_ex)
if type_ex == 'минимум':
    ak_values, bk_values, x_values = golden_ratio(a0, b0, f, eps)
else:
    ak_values, bk_values, x_values = golden_ratio(a0, b0, negative_f, eps)
print(f'x* = {x_values[-1]:.6f} y* = {f(x_values[-1]):.6f}')

table = []
for i in range(len(x_values)):
    table.append([i, ak_values[i], bk_values[i], x_values[i]])
print(tabulate(table, headers=["Итерация", "a", "b", "x"], tablefmt="pretty"))
