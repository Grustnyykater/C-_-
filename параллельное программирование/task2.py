
import numpy as np
from multiprocessing import Pool, Value
import os
import random

# Глобальный флаг для остановки процесса
stop_flag = Value('i', 0)


def read_matrix_from_file(filename):
    """Чтение матрицы из файла."""
    return np.loadtxt(filename)


def write_matrix_to_file(matrix, filename):
    """Запись матрицы в файл."""
    np.savetxt(filename, matrix)


def write_element_to_file(value, index):
    """Запись элемента в промежуточный файл."""
    with open('intermediate_results.txt', 'a') as f:
        f.write(f"Элемент {index}: {value}\n")


def element(index, A, B):
    """Вычисление одного элемента результирующей матрицы и запись в файл."""
    if stop_flag.value:
        return None  # Завершение работы, если установлен флаг остановки
    i, j = index
    value = sum(A[i][k] * B[k][j] for k in range(len(A[0])))
    write_element_to_file(value, index)
    return value


def compute_matrix_product(A, B):
    """Вычисление произведения матриц A и B."""
    rows_A, cols_A = A.shape
    rows_B, cols_B = B.shape
    if cols_A != rows_B:
        raise ValueError("Количество столбцов первой матрицы должно совпадать с количеством строк второй матрицы.")

    # Создаем пустую матрицу для результата
    result = np.zeros((rows_A, cols_B))

    # Генерируем индексы для всех элементов результирующей матрицы
    indices = [(i, j) for i in range(rows_A) for j in range(cols_B)]

    # Используем пул процессов для вычисления элементов
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.starmap(element, [(index, A, B) for index in indices])

    # Заполняем результирующую матрицу
    for idx, value in zip(indices, results):
        if value is not None:  # Проверка на None, если процесс был остановлен
            result[idx] = value

    return result


def generate_random_matrix(size):
    """Генерация случайной квадратной матрицы заданного размера."""
    return np.random.rand(size, size)


def async_matrix_multiplication(size):
    """Асинхронное перемножение случайных матриц."""
    A = generate_random_matrix(size)
    B = generate_random_matrix(size)
    result_matrix = compute_matrix_product(A, B)
    write_matrix_to_file(result_matrix, 'result_matrix.txt')


if __name__ == "__main__":
    size = int(input("Введите размер квадратной матрицы: "))

    # Запуск асинхронного перемножения
    async_matrix_multiplication(size)

    # Пример остановки процесса
    stop = input("Введите 'stop' для остановки процесса: ")
    if stop.lower() == 'stop':
        stop_flag.value = 1
        print("Процесс остановлен.")