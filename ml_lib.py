import numpy as np

from fixed_float import FixedHomoFloat

def matmul(lhs, rhs):
    assert lhs.shape[1] == rhs.shape[0]

    output_matrix = []

    for i in range(lhs.shape[0]):
        output_matrix.append([])
        for j in range(rhs.shape[1]):
            output_matrix[i].append(FixedHomoFloat(0))
            for k in range(lhs.shape[1]):
                output_matrix[i][j] += lhs[i, k] * rhs[k, j]

    return output_matrix