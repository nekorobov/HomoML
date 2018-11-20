import numpy as np

from fixed_float import FixedHomoFloat, make_array
from sklearn.datasets import make_regression
from ml_lib import LinearRegression, matmul, MatrixWrapper
import matplotlib.pyplot as plt

arr1 = make_array([
    [1, 0],
    [0, 1]
])
arr2 = arr1.copy()
assert np.all(arr1 == arr2)
assert np.all(matmul(arr1, arr2) == arr1)
assert np.all(arr1 * arr2 == arr1)
assert np.all(2 * (arr1 + arr1[:, [1, 0]]) - 3 / (arr2 + arr2[:, [1, 0]]) == -(arr1 + arr1[:, [1, 0]]))
assert np.all(-3.5 * arr1 * 2 == -7 * arr1)
assert np.all(arr1 >= arr2)
assert np.all(2 * (arr1 + arr1[:, [1, 0]]) > arr2)

mtx = make_array([[1, 1], [0, 2]])
hnd = MatrixWrapper(mtx)
#assert np.all(matmul(hnd.invert(), mtx) == make_array(np.eye(2)))

clf = LinearRegression(C=1)

X, y = make_regression(n_samples=10, n_features=1)

X_cyphered, y_cyphered = map(make_array, (X, y))

clf.fit(X, y)
print(clf.predict(X))
plt.scatter(X, y, color='r')
plt.scatter(X, [-46.313340453152,
 -70.53575303326465,
 -61.16842077094948,
 -35.84238122253395,
 -41.27146565829159,
 -70.54638431361396,
 -57.12643548402897,
 -30.3011448107672,
 -4.25598140463259,
 -77.51488545419554,
 -24.759481092763135,
 -13.00253809202784,
 -33.55695685850926,
 -96.0896009684382,
 -77.71028653262292,
 -49.20738400443942,
 -79.46788263536456,
 -82.20573227475592,
 -42.89563605806039,
 -39.96461099242543], color='b')
plt.show()

print(y)
