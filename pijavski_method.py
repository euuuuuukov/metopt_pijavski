from typing import Callable
import numpy as np
import matplotlib.pyplot as plt
from time import time
from math import log10


def pijavski_method(f: Callable[[float], float], a: float, b: float, l: float, eps: float) -> None:
    start_time = time()

    x_points = [a, b]
    y_points = [f(a), f(b)]

    iterations = 0

    while True:
        iterations += 1

        points = sorted(zip(x_points, y_points))
        x_points_sorted = [i[0] for i in points]
        y_points_sorted = [i[1] for i in points]

        min_p_value = float('inf')
        next_point = None

        for i in range(len(x_points_sorted) - 1):
            x1, x2 = x_points_sorted[i], x_points_sorted[i + 1]
            y1, y2 = y_points_sorted[i], y_points_sorted[i + 1]

            x_intersect = (y1 - y2 + l * (x1 + x2)) / (2 * l)

            p_value = (y1 + y2 - l * (x2 - x1)) / 2

            if x1 < x_intersect < x2 and p_value < min_p_value:
                min_p_value = p_value
                next_point = x_intersect

        if next_point is None:
            max_interval = 0
            for i in range(len(x_points_sorted) - 1):
                interval = x_points_sorted[i + 1] - x_points_sorted[i]
                if interval > max_interval:
                    max_interval = interval
                    next_point = (x_points_sorted[i + 1] + x_points_sorted[i]) / 2

        x_points.append(next_point)
        y_points.append(f(next_point))

        # Вычисляем текущий минимум и оценку погрешности
        current_min = min(y_points)

        # Пересчитываем минимальное значение ломаной для оценки погрешности
        min_p_overall = float('inf')
        for i in range(len(x_points_sorted) - 1):
            x1, x2 = x_points_sorted[i], x_points_sorted[i + 1]
            y1, y2 = y_points_sorted[i], y_points_sorted[i + 1]
            p_value = (y1 + y2 - l * (x2 - x1)) / 2
            if p_value < min_p_overall:
                min_p_overall = p_value

        # Условие остановки: разница между текущим минимумом и минимальным значением ломаной
        error = current_min - min_p_overall if min_p_overall > -float('inf') else float('inf')

        if error < eps:
            break

    best_y = min(y_points)
    best_x = x_points[y_points.index(best_y)]

    all_time = time() - start_time

    rounding = int(log10(1 / eps))

    print(f'Результаты нахождения глобального минимума ({f.__name__}, L = {l}, a = {a}, b = {b})')
    print(f'Приближенное значение аргумента x_min = {best_x:.{rounding}f}, f(x_min) = {best_y:.{rounding}f}.')
    print(f'Число пробовавшихся итераций: {iterations}, затраченное время: {all_time:.3f} с.')

    plt.figure(figsize=(12, 6))

    x_plot_list = []
    y_plot_list = []
    step = (b - a) / 500.0
    for i in range(501):
        x_val = a + i * step
        x_plot_list.append(x_val)
        y_plot_list.append(f(x_val))

    x_plot = np.array(x_plot_list)
    y_plot = np.array(y_plot_list)

    plt.plot(x_plot, y_plot, 'b-', label=f'Функция {f.__name__}', linewidth=2)

    # График итоговой ломаной (используем numpy для отрисовки списков)
    final_points = sorted(zip(x_points, y_points))
    final_x = np.array([p[0] for p in final_points])
    final_y = np.array([p[1] for p in final_points])
    plt.plot(final_x, final_y, 'g--', label='Итоговая ломаная Пиявского', alpha=0.6, marker='o', markersize=4)

    # Вспомогательные функции (нижняя огибающая)
    for i in range(len(final_x) - 1):
        x1, x2 = final_x[i], final_x[i + 1]
        y1, y2 = final_y[i], final_y[i + 1]
        x_seg = np.linspace(x1, x2, 100)
        y_seg = np.maximum(y1 - l * np.abs(x_seg - x1), y2 - l * np.abs(x_seg - x2))
        plt.plot(x_seg, y_seg, 'r-', alpha=0.3)

    # Указание найденной точки минимума
    plt.scatter(best_x, best_y, color='red', marker='*', s=50, zorder=10, label='Найденный минимум')
    plt.axvline(best_x, color='red', linestyle=':', ymax=0.5)

    plt.title(f'Метод Пиявского: {f.__name__} на отрезке [{a}, {b}] (L = {l}, eps = {eps})')
    plt.xlabel('X')
    plt.ylabel('f(X)')
    plt.legend()
    plt.grid(True)
    plt.show()
