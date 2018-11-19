from fixed_float import FixedHomoFloat
import numpy as np

a = FixedHomoFloat(-128, k=1)
b = FixedHomoFloat(100, k=0)

c = a + b

print(c.get_value())

c = a - b

print(c.get_value())

c = a * b

print(c.get_value())

c = a / b

print(c.get_value())

print(a > b)
print(a <= b)
print(a == b)

arr1 = np.array([
    [FixedHomoFloat(1), FixedHomoFloat(0)],
    [FixedHomoFloat(0), FixedHomoFloat(1)],
])
arr2 = np.array([
    [FixedHomoFloat(1), FixedHomoFloat(0)],
    [FixedHomoFloat(0), FixedHomoFloat(1)],
])

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

print(matmul(arr1, arr2))

print(-1 * arr1)
print(1 / arr1)