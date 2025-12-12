import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from simulation_modeling import z


# Константы
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

# Расчёт констант скоростей реакций по уравнению Аррениуса
k1 = A1 * np.exp(-E1 / (R*T))
k2 = A2 * np.exp(-E2 / (R*T))
k3 = A3 * np.exp(-E3 / (R*T))

print("k1 =", k1, "k2 =", k2, "k3 =", k3)

# Расчет массового расхода реакционной среды, кг/с.
m = m_c1 + m_O2

# Расчет скорости движения реакционной среды через аппарат
u = (4 * m) / (ro*np.pi*D**2)
print("u", u)

L = 3.47  # длина трубы найденная на этапе оптимизации
tau_max = 200
tau_s = L / u  # среднее время пребывания

d_alpha = 0.3
d_beta = 0.2


def dC1_dalpha(C1):
    # Правая часть уравнения для dC1/dalpha.
    # C1 — концентрация бензола, моль/м^3.
    return -C1*(k1 + k3)


def dC2_dalpha(C1, C2):
    # Правая часть уравнения для dC2/dalpha.
    # C1 — концентрация бензола, моль/м^3.
    # C2 — концентрация малеинового ангидрида, моль/м^3.
    return k1*C1 - k2*C2


def f_Cvh(tau):
    # Функция граничного условия С1вх(tau) на основе случайного процесса z
    return z[int(tau)]


data = []
data2 = []

C1_show = []
C2_show = []
tau_show = []


def integrate(C1_initial, C2_initial, alpha_start, alpha_end, step, beta):
    C1 = C1_initial
    C2 = C2_initial
    alpha = alpha_start
    while alpha <= alpha_end:
        C1_0 = C1
        C1 += dC1_dalpha(C1) * step
        C2 += dC2_dalpha(C1_0, C2) * step
        l = u * (alpha - beta)
        tau = alpha + beta
        alpha += step
        data.append((tau, l, C1))
        data2.append((tau, l, C2))

    return C1, C2, tau


# Область II: beta ∈ [0, (tau_max-tau_s)/2]
for beta in np.arange(0, (tau_max-tau_s)/2, d_beta):
    alpha_start = beta
    alpha_end = beta + tau_s
    print("2*beta",2*beta)
    C1_initial = f_Cvh(2*beta)
    C1_final, C2_final, tau = integrate(C1_initial, 0, alpha_start, alpha_end, d_alpha, beta)
    C1_show.append(C1_initial)
    C2_show.append(C2_final)
    tau_show.append(tau)


# Область III: beta ∈ [(tau_max-tau_s)/2, tau_max/2]
for beta in np.arange((tau_max-tau_s)/2, tau_max/2, d_beta):
    alpha_start = beta
    alpha_end = -beta + tau_max
    C1_initial = f_Cvh(2 * beta)
    C1_final, C2_final, tau = integrate(C1_initial, 0, alpha_start, alpha_end, d_alpha, beta)
    C1_show.append(C1_initial)
    C2_show.append(C2_final)
    tau_show.append(tau)

print("C2", C2_show)
print("tau", tau_show)


# Построение графиков
plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(z)
plt.grid(True)
plt.xlabel('$τ (с)$')
plt.ylabel('C1')
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)

plt.subplot(2, 1, 2)
plt.plot(tau_show, C2_show)
plt.plot([tau_s, tau_s], [0, C2_show[int(tau_s)]], label="Среднее время пребывания")
plt.legend()
plt.grid(True)
plt.xlabel('$τ (с)$')
plt.ylabel('C2')
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)

plt.tight_layout()
plt.show()

