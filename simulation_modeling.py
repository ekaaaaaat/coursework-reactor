import numpy as np
import matplotlib.pyplot as plt
import math

# исходные параметры случайного процесса
lambda1 = math.pow(5, 11)
lambda2 = math.pow(2, 18)

N = 210  # длина ряда случайных чисел
Kz_num = 20
Z0 = 1  # первое число ряда

# параметры, определяемые для каждого конкретного генератора случайных чисел
A1 = 1
A2 = 1

Ns = 10  # количество суммируемых членов ряда х

M0 = 770  # (моль/м^3) мат.ожидание
sigma0_2 = 400  # дисперсия
alpha0 = 0.09  # параметр аппроксимации


def generation_congurent_method(n, lam1, lam2, x0):
    # Функция генерации случайных чисел (Конгруэнтный метод)
    x = [x0]
    for i in range(1, n):
        x.append((lam1 * x[i-1]) % lam2)
    x_norm = [xi / lam2 - 0.5 for xi in x]  # нормализация в [-0.5; 0.5]
    return x_norm


def checkmate_waiting(z):
    # Математическое ожидание
    return sum(z) / len(z)


# Дисперсия
def dispersion(z, M):
    return sum([(i - M)**2 for i in z]) / len(z)


# Основная программа
x = generation_congurent_method(N, lambda1, lambda2, Z0)
print(x)

Mx = checkmate_waiting(x)
sigma_x2 = dispersion(x, Mx)
print(Mx, sigma_x2)

# # Центрирование, если Mx ≠ 0
if abs(Mx) > 1e-6:
    x = [xi - Mx for xi in x]
    Mx = checkmate_waiting(x)
    sigma_x2 = dispersion(x, Mx)

print(x)
print(Mx, sigma_x2)
