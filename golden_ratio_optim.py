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


def graf(a_, b_, f_, ak, bk, x):
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid()
    k = np.linspace(a_ - 0.1, b_ + 0.1, 1000)
    plt.plot(k, f_(k), color='purple', linewidth=2.0, label='Целевая функция')
    plt.plot([x[0], x[0]], [f_(x[0]), -5], color='g', ls='--', linewidth=2.0, marker='x', markersize=7, label='x*')
    plt.plot([ak[0], ak[0]], [f_(ak[0]), -5], color='hotpink', ls='--', linewidth=1.0, marker='o', markersize=4, label='ak')
    plt.plot([bk[0], bk[0]], [f_(bk[0]), -5], color='aqua', ls='--', linewidth=1.0, marker='o', markersize=4, label='bk')

    for j in range(1, len(x)):
        plt.plot([x[j], x[j]], [f_(x[j]), -5], color='g', ls='--', linewidth=2.0, marker='x', markersize=7)
        plt.plot([ak[j], ak[j]], [f_(ak[j]), -5], color='hotpink', ls='--', linewidth=1.0, marker='o', markersize=4)
        plt.plot([bk[j], bk[j]], [f_(bk[j]), -5], color='aqua', ls='--', linewidth=1.0, marker='o', markersize=4)
    plt.legend()

    plt.plot(x[-1], f_(x[-1]), color='red', linewidth=3.0, marker='o', markersize=10)

    plt.show()


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
graf(a0, b0, f, ak_values, bk_values, x_values)
