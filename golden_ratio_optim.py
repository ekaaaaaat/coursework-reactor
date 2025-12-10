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