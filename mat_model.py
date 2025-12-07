import matplotlib.pyplot as plt
import numpy as np
import math

# Физические константы и параметры задачи

R = 8.31  # универсальная газовая постоянная, Дж/(моль·К)

# Предэкспоненциальный множитель и энергия активации уравнения Аррениуса для вычисления константы скорости i-й реакции
A1 = 92 * 10**8
E1 = 150000  # Дж/моль
A2 = 16*10**7
E2 = 132000  # Дж/моль
A3 = 580
E3 = 60000  # Дж/моль

# Геометрические и технологические параметры
D = 0.12  # диаметр трубы, м
T = 640  # температура, К
m_c1 = 0.015  # массовый расход бензола на входе, кг/с
m_O2 = 0.035  # массовый расход кислорода на входе, кг/с
ro = 200  # средняя плотность реакционной среды, кг/м^3

# Молярные массы компонентов
mu_C1 = 0.078  # бензол, кг/моль
mu_C2 = 0.098  # малеиновый ангидрид, кг/моль

# Варьируемый параметр и шаг по длине
L = 5  # длина трубы, м (тестовое значение)
d_l = 0.01  # шаг интегрирования по длине, м


# Расчёт констант скоростей реакций по уравнению Аррениуса
k1 = A1 * math.exp(-E1 / (R*T))
k2 = A2 * np.exp(-E2 / (R*T))
k3 = A3 * np.exp(-E3 / (R*T))

print("k1 =", k1, "k2 =", k2, "k3 =", k3)


def percent_C(C_m, mu):
    # Перевод концентрации из моль/м^3 в %.

    C = (C_m * 100 * mu) / ro
    return C


def f_C1(C1, m):
    # Правая часть уравнения для dC1/dl.
    # C1 — концентрация бензола, моль/м^3.
    # m — массовый расход реакционной среды, кг/с.

    C1 = (-C1 * (k1 + k3) * ro * np.pi * (D ** 2)) / (4 * m)
    return C1


def f_C2(C1, C2, m):
    # Правая часть уравнения для dC2/dl.
    # C1 — концентрация бензола, моль/м^3.
    # C2 — концентрация малеинового ангидрида, моль/м^3.
    # m — массовый расход реакционной среды, кг/с.

    C2 = ((k1 * C1 - k2 * C2) * ro * np.pi * (D ** 2)) / (4 * m)
    return C2


# Расчет входной концентрации бензола
C1 = (m_c1 * ro) / ((m_c1+m_O2) * mu_C1)

# Расчет массового расхода реакционной среды, кг/с.
m0 = m_c1+m_O2

C2 = 0
l = 0

# Массивы для сохранения концентраций
C1_val = [C1]
C2_val = [C2]
C1_proc = percent_C(C1, mu_C1)
C2_proc = percent_C(C2, mu_C2)
C1_percent_array = [C1_proc]
C2_percent_array = [C2_proc]
l_val = [l]

print(f"Концентрация бензола на входе: {C1_val[0]} моль/м^3, {C1_percent_array[0]} %")
print("m0 =", m0)

# Численное интегрирование по длине трубы методом Эйлера
while l < L:
    C1_0 = C1
    C1 += f_C1(C1, m0) * d_l
    C2 += f_C2(C1_0, C2, m0) * d_l
    l += d_l

    C1_val.append(C1)
    C2_val.append(C2)
    C1_proc = percent_C(C1, mu_C1)
    C2_proc = percent_C(C2, mu_C2)
    C1_percent_array.append(C1_proc)
    C2_percent_array.append(C2_proc)
    l_val.append(l)

print(f"Концентрация малеинового ангидрида на выходе: {C2_val[-1]} моль/м^3, {C2_percent_array[-1]} %")
print(f"Длина трубы: {l_val[-1]} м")

# Построение графиков концентраций
plt.subplot(1, 2, 1)
plt.plot(l_val, C1_percent_array)
plt.grid(True)
plt.xlabel('$l, м$')
plt.ylabel('C1,%')
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)

plt.subplot(1, 2, 2)
plt.plot(l_val, C2_percent_array)
plt.grid(True)
plt.xlabel('$l, м$')
plt.ylabel('C2,%')
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)

plt.tight_layout()
plt.show()
