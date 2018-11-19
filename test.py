import numpy as np

from fixed_float import FixedHomoFloat, make_array
from sklearn.datasets import make_regression
from ml_lib import LinearRegression, matmul, MatrixWrapper

arr1 = make_array([
    [1, 0],
    [0, 1]
])
arr2 = arr1.copy()

assert np.all(arr1 == arr2)
assert np.all(matmul(arr1, arr2) == arr1)
assert np.all(arr1 * arr2 == arr1)
assert np.all(2 * (arr1 + arr1[:, [1, 0]]) - 3 / (arr2 + arr2[:, [1, 0]]) == -(arr1 + arr1[:, [1, 0]]))
#assert np.all(-3.5 * arr1 * 2 == -7 * arr1)
assert np.all(arr1 >= arr2)
assert np.all(2 * (arr1 + arr1[:, [1, 0]]) > arr2)

mtx = make_array([[1, 1], [0, 2]])
hnd = MatrixWrapper(mtx)
#assert np.all(matmul(hnd.invert(), mtx) == make_array(np.eye(2)))

clf = LinearRegression(C=1)

X, y = make_regression(n_samples=10, n_features=10)

X_cyphered, y_cyphered = map(make_array, (X, y))

clf.fit(X, y)
print('asdds')
print(clf.predict(X))
print(y)
