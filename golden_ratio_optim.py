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

