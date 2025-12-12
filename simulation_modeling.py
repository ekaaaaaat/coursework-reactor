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


# Корреляционная функция
def correlation_function(z, M, Smax):
    N = len(z)
    K = []
    for S in range(Smax):
        ssum = 0
        for i in range(N - S):
            ssum += (z[i] - M) * (z[i + S] - M)
        K.append(ssum / (N - S))
    return K


# Аппроксимация
def approximate_alpha(S, K, sig_2, max_iter=1000):
    alph = []
    for i in range(len(S)):
        alp = 1
        kt = sig_2 * math.exp(-alp * abs(S[i]))
        iter_count = 0
        while kt < abs(K[i]) and iter_count < max_iter:
            alp -= 0.1
            kt = sig_2 * math.exp(-alp * abs(S[i]))
            iter_count += 1
        alph.append(max(alp, 0.001))  # не даем alpha быть отрицательной

    alph_final = sum(alph) / len(alph)
    k_appr = [sig_2 * math.exp(-alph_final * abs(S[i])) for i in range(len(S))]
    return alph_final, k_appr


def generate_process_z(x, A1, A2, sigma0_2, sigma_x0_2, alpha0, M0, Ns):
    # Функция генерации случайного процесса
    z = []
    for k in range(len(x) - Ns):
        ssum = 0
        for i in range(k, k + Ns):
            ssum += x[i] * math.sqrt(sigma0_2 / (sigma_x0_2 * alpha0 * A2)) * A1 * math.exp(-A2 * alpha0 * abs(i - k))
        z.append((1 / Ns) * ssum + M0)
    return z


# Подбор A1, A2 методом градиентного спуска
def gradient_search(x, sigma_x2, M0, sigma0_2, alpha0, Ns,
                    A1_init=1.0, A2_init=1.0,
                    lr=0.01, delta=0.05,
                    max_iter=1000, tol=0.1):

    def process_error(A1, A2):
        z = generate_process_z(x, A1, A2, sigma0_2, sigma_x2, alpha0, M0, Ns)
        Mz = checkmate_waiting(z)
        sigma_z2 = dispersion(z, Mz)
        Kz = correlation_function(z, Mz, Kz_num)
        alpha_z, _ = approximate_alpha(range(Kz_num), Kz, sigma_z2)
        err = abs((Mz - M0)/M0) + abs((sigma_z2 - sigma0_2)/sigma0_2) + abs((alpha_z - alpha0)/alpha0)
        return err

    A1, A2 = A1_init, A2_init
    best_err = process_error(A1, A2)

    for iteration in range(max_iter):
        # численные производные
        E0 = process_error(A1, A2)

        E_A1_plus = process_error(A1 + delta, A2)
        E_A1_minus = process_error(A1 - delta, A2)
        grad_A1 = (E_A1_plus - E_A1_minus) / (2 * delta)

        E_A2_plus = process_error(A1, A2 + delta)
        E_A2_minus = process_error(A1, A2 - delta)
        grad_A2 = (E_A2_plus - E_A2_minus) / (2 * delta)

        # обновляем A1, A2
        A1 -= lr * grad_A1
        A2 -= lr * grad_A2

        # пересчёт ошибки
        err = process_error(A1, A2)

        if err < best_err:
            best_err = err

        # Условие выхода
        if err < tol or best_err < 0.1:
            break

    return A1, A2


# Основная программа
x = generation_congurent_method(N, lambda1, lambda2, Z0)
# print(x)

Mx = checkmate_waiting(x)
sigma_x2 = dispersion(x, Mx)
# print(Mx, sigma_x2)

# # Центрирование, если Mx ≠ 0
if abs(Mx) > 1e-6:
    x = [xi - Mx for xi in x]
    Mx = checkmate_waiting(x)
    sigma_x2 = dispersion(x, Mx)

# print(x)
# print(Mx, sigma_x2)

# Генерация процесса z
z = generate_process_z(x, A1, A2, sigma0_2, sigma_x2, alpha0, M0, Ns)
# print(z)

# Характеристики процесса
Mz = checkmate_waiting(z)
sigma_z2 = dispersion(z, Mz)
Kz = correlation_function(z, Mz, Kz_num)
alpha_z, K_apr = approximate_alpha(range(Kz_num), Kz, sigma_z2)
# print("Kz", Kz)

# ВЫВОД1
print(f"Mx = {Mx:.4f}")
print(f"sigma_x^2 = {sigma_x2:.4f}")
print(f"Mz = {Mz:.4f}")
print(f"sigma_z^2 = {sigma_z2:.4f}")
print(f"alpha_z = {alpha_z:.4f}")
print(f"A1 = {A1:.4f}, A2 = {A2:.4f}")


# Проверка 10%-ного отклонения
def is_within_tolerance(value, target, tol=0.1):
    return abs((value - target) / target) <= tol


if not (is_within_tolerance(Mz, M0) and
        is_within_tolerance(sigma_z2, sigma0_2) and
        is_within_tolerance(alpha_z, alpha0)):
    print("Отклонение более 10%. Запускаем градиентный спуск...")
    A1, A2 = gradient_search(x, sigma_x2, M0, sigma0_2, alpha0, Ns)
    z = generate_process_z(x, A1, A2, sigma0_2, sigma_x2, alpha0, M0, Ns)
    Mz = checkmate_waiting(z)
    sigma_z2 = dispersion(z, Mz)
    Kz = correlation_function(z, Mz, Kz_num)
    alpha_z, K_apr = approximate_alpha(range(Kz_num), Kz, sigma_z2)


# ВЫВОД2
print(f"Mx = {Mx:.4f}")
print(f"sigma_x^2 = {sigma_x2:.4f}")
print(f"Mz = {Mz:.4f}")
print(f"sigma_z^2 = {sigma_z2:.4f}")
print(f"alpha_z = {alpha_z:.4f}")
print(f"A1 = {A1:.4f}, A2 = {A2:.4f}")


#ГРАФИКИ
fig, axs = plt.subplots(3, 1, figsize=(7, 7))

axs[0].plot(x, color='magenta')
axs[0].set_title("Ряд случайных чисел (конгруэнтный метод)")
axs[0].grid()

axs[1].plot(z, color='green')
axs[1].set_title("Случайный процесс z(k)")
axs[1].grid()

S = np.arange(Kz_num)
axs[2].plot(S, Kz, 'bo-', label='Kz(S)')
axs[2].plot(S, K_apr, 'r--', label='sigma_z2 * exp(-αS)')
axs[2].legend()
axs[2].set_title("Корреляционная функция и аппроксимация")
axs[2].grid()

plt.tight_layout()
plt.show()
