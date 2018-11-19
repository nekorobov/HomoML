import numpy as np

from fixed_float import FixedHomoFloat, make_array
from ml_lib import matmul

arr1 = make_array([
    [1, 0],
    [0, 1]
])
arr2 = arr1.copy()

assert np.all(arr1 == arr2)
assert np.all(matmul(arr1, arr2) == arr1)
assert np.all(arr1 * arr2 == arr1)
assert np.all(2 * (arr1 + arr1[:, [1, 0]]) - 3 / (arr2 + arr2[:, [1, 0]]) == -(arr1 + arr1[:, [1, 0]]))
# assert np.all((-3.5 * arr1 * 2 == 7 * arr1))
assert np.all(arr1 >= arr2)
assert np.all(2 * (arr1 + arr1[:, [1, 0]]) > arr2)