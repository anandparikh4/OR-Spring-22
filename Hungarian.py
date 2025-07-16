"""
  Author  : Abhay Kumar Keshari
  Roll No : 20CS10001
  Date    : Spring 2022
  Course  : Operation Research MA30014
"""

import numpy as np


def scanner():
    rows = int(input())
    matrix = np.array([input().strip().split() for _ in range(rows)], float)
    (row, col) = matrix.shape
    if row > col:
        padding = ((0, 0), (0, row - col))
    else:
        padding = ((0, col - row), (0, 0))
    matrix = np.pad(matrix, padding, mode='constant', constant_values=0)
    assert matrix.shape[0] == matrix.shape[1]
    return matrix


def cost(matrix, path):
    cost = 0
    print("\n\nOptimal Assignment:")
    for i in range(len(matrix)):
        print("Worker", i + 1, "--> Job", path[i] + 1, "| Cost : ", matrix[i][path[i]])
        cost += matrix[i][path[i]]
    print("Total Minimum cost:", cost)


def row_reduction(matrix):
    assert isinstance(matrix, np.matrixlib.defmatrix.matrix)
    matrix -= np.min(matrix, axis=1)
    return matrix


def col_reduction(matrix):
    assert isinstance(matrix, np.matrixlib.defmatrix.matrix)
    matrix -= np.min(matrix, axis=0)
    return matrix


def find_filter(matrix, max_filter=6):
    paths = {'path': []}

    def redundant_index(vec):
        frequency_vec = [vec.count(i) for i in range(len(vec))]
        return max(frequency_vec) - 1 + frequency_vec.count(0) * 1.0 / len(vec)

    def path_recorder(vec):
        ridx = redundant_index(vec)
        paths['path'] = paths['path'] + [vec] + [ridx]

    def search_paths(m, tracer):
        col = m.shape[1]
        tracing_number = len(tracer)
        if col > tracing_number:
            col_index_arranged = list(set(range(col)) - set(tracer)) + list(set(tracer))
            for entries in col_index_arranged:
                if m[tracing_number, entries] == 0:
                    if len(paths['path']) < 2 * max_filter:
                        search_paths(m, tracer + [entries])
        elif tracing_number == col:
            path_recorder(tracer)

    is_zero = True
    for j in range(matrix.shape[1]):
        if matrix[0, j] == 0:
            if is_zero:
                paths['path'] = []
                is_zero = False
            search_paths(matrix, [j])

    if len(paths['path']) == 0:
        raise TypeError('Input matrix does not have any 0-filters.')
    return [matrix, paths['path']]


def is_optimal(cost_matrix, paths_):
    """
    :param cost_matrix: cost matrix
    :param paths_: list of 0-filter followed by its index of redundancy
    as returned by find_filter
    :return: cost_matrix , followed by the list of 0-filter with
    minimal index of redundancy, and a flag, True if the minimal index
    is 0, False otherwise.
    """
    min_redundancy = np.min(paths_[1::2])
    filtered_path = [paths_[i] for i in list(range(len(paths_)))[::2] if paths_[i + 1] == min_redundancy]
    flag = (min_redundancy == 0)
    return [cost_matrix, filtered_path, flag]


def mix_matrix(matrix, filtered_paths):
    row, col = matrix.shape
    min_redundancy_filter = filtered_paths[0]

    [cov_row, cov_col] = covering_segments_searcher(matrix, min_redundancy_filter)

    zeroes_in_cov_row = [i for i in range(row) if cov_row[i] == 0]
    zeroes_in_cov_col = [j for j in range(col) if cov_col[j] == 0]
    uncovered_elements = [matrix[i, j] for i in zeroes_in_cov_row for j in zeroes_in_cov_col]
    if not uncovered_elements:
        raise EnvironmentError('Not enough filters has been considered, ' 'set an higher max_num_filter parameter!')

    minimum_value = min(uncovered_elements)

    for i in range(row):
        for j in range(col):
            if cov_row[i] == 1 == cov_col[j]:
                matrix[i, j] += 2 * minimum_value
            elif cov_row[i] == 0 == cov_col[j]:
                matrix[i, j] -= minimum_value
    return matrix


def covering_segments_searcher(matrix, min_redundancy_filter):
    row, col = matrix.shape
    marked_row = [0] * row
    marked_col = [0] * col

    frequency_vector = [min_redundancy_filter.count(i) for i in range(row)]
    for i in range(row):
        if frequency_vector[i] > 1:
            duplicates = [k for k in range(row) if min_redundancy_filter[k] == i][1:]
            for j in duplicates:
                marked_row[j] = 1
    mark = 1
    while mark != 0:
        mark = 0
        for i in range(row):
            if marked_row[i] == 1:
                for j in range(col):
                    if matrix[i, j] == 0 and marked_col[j] != 1:
                        marked_col[j] = 1
                        mark *= 2
        for j in range(col):
            if marked_col[j] == 1:
                for i in range(row):
                    if matrix[i, j] == 0 and marked_row[i] != 1 and min_redundancy_filter[i] == j:
                        marked_row[i] = 1
                        mark += 1
    covered_row = [(i + 1) % 2 for i in marked_row]
    covered_col = marked_col

    return covered_row, covered_col


def hungarian_method(matrix, max_num_filter=100):
    count = 0
    max_loop = max(matrix.shape[0], matrix.shape[1])
    s = row_reduction(matrix)
    s = col_reduction(s)
    [s, paths] = find_filter(s, max_filter=max_num_filter)
    [s, filtered_paths, flag] = is_optimal(s, paths)
    while not flag and count < max_loop:
        s = mix_matrix(s, filtered_paths)
        [s, paths] = find_filter(s, max_filter=max_num_filter)
        [s, filtered_paths, flag] = is_optimal(s, paths)
        count += 1
    solutions = []
    for _paths in filtered_paths:
        sol = []
        for i in range(len(matrix)):
            sol.append(("Worker:" + str(i), "Job:" + str(_paths[i])))
        solutions.append(sol)

    for i, sol in enumerate(solutions):
        print("Solution", i + 1)
        print(sol)
    return filtered_paths


if __name__ == '__main__':
    m = scanner()
    path = hungarian_method(np.matrix(m), 10)
    cost(m, path[0])
