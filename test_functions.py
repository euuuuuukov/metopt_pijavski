from math import *


def example_function(x: float) -> float:
    """
    Тестовая функция из задания.
    b - a >= 2pi, L = 4.1416.
    """
    return x + sin(pi * x)


def rastrigin_function(x: float) -> float:
    """
    Функция Растригина.
    a = -5.12, b = 5.12, L = 63.334.
    """
    return 10 + x ** 2 - 10 * cos(2 * pi * x)


def ackley_function(x: float) -> float:
    """
    Функция Экли.
    a = -5, b = 5, L = 6.274.
    """
    return -20 * exp(-0.2 * abs(x) * sqrt(0.5)) - exp(0.5 * cos(2 * pi * x)) + e + 20

def easom_function(x: float) -> float:
    """
    Функция Изома.
    a = -100, b = 100, L = 0.0154.
    """
    return cos(x) * exp(-((x - pi) ** 2))
