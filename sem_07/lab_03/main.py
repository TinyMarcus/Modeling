from random import random
from numpy import linalg
from prettytable import PrettyTable


TIME_DELTA = 1e-3
EPS = 1e-3


def get_rand_matrix(size):
    matrix = [[None for j in range(size)] for i in range(size)]
    
    for i in range(size):
        for j in range(size):
            if i != j:
                matrix[i][j] = round(random(), 4)
            else:
                matrix[i][j] = 0.0
    return matrix


def get_coeffs(matrix):
    n = len(matrix)
    lst = [[None for j in range(n)] for i in range(n)]

    for i in range(n):
        if i != (n - 1):
            for j in range(n):
                if j != i:
                    lst[i][j] = matrix[j][i]
                else:
                    lst[i][j] = -sum(matrix[i])
        else:
            for j in range(n):
                lst[i][j] = 1
    return lst


def get_limit_probabilities(matrix):
    coeffs = get_coeffs(matrix)
    return linalg.solve(coeffs, [0 if i != (len(matrix) - 1) else 1 for i in range(len(matrix))]).tolist()


def get_probability_increments(matrix, start_probabilities):
    n = len(matrix)
     
    return [TIME_DELTA * sum([-sum(matrix[i]) * start_probabilities[j] if i == j
            else matrix[j][i] * start_probabilities[j] for j in range(n)]) for i in range(n)]


def get_limit_times(matrix, limit_probabilities):
    n = len(matrix)
    start_probabilities = [None] * n
    limit_times = [0.0] * n
    current_time = 0.0

    for i in range(n):
        start_probabilities[i] = 1.0 / n

    current_probabilities = start_probabilities.copy()

    while not all(limit_times):
        dp = get_probability_increments(matrix, start_probabilities)
        for i in range(n):
            if not limit_times[i] and abs(current_probabilities[i] - limit_probabilities[i]) <= EPS:
                limit_times[i] = current_time
            current_probabilities[i] += dp[i]
            current_time += TIME_DELTA
    return limit_times


def calculate(matrix):
    limit_p = [round(x, 4) for x in get_limit_probabilities(matrix)]
    limit_t = [round(x, 4) for x in get_limit_times(matrix, limit_p)]
    return limit_p, limit_t


def output(matrix, res_p, res_t):
    table_matrix = PrettyTable()
    cols = ["States"]
    cols.extend([str(i + 1) for i in range(len(matrix))])
    table_matrix.field_names = cols

    for i in range(len(matrix)):
        tmp = [item for item in matrix[i]]
        tmp.insert(0, i + 1)
        table_matrix.add_row(tmp)
    print(table_matrix)
    print()

    table_res = PrettyTable()
    table_res.add_column("States", [i + 1 for i in range(len(res_p))])
    table_res.add_column("Marginal probability", res_p)
    table_res.add_column("Time", res_t)
    print(table_res)


def main():
    size = int(input("Input size of system: "))
    matrix = get_rand_matrix(size)
    res_p, res_t = calculate(matrix)
    output(matrix, res_p, res_t)


if __name__ == '__main__':
    main()