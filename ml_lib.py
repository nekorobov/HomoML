import numpy as np

from sklearn.base import BaseEstimator, ClassifierMixin
from tqdm import tqdm
from fixed_float import FixedHomoFloat, make_array


def matmul(lhs, rhs):
    assert lhs.shape[1] == rhs.shape[0]

    output_matrix = []

    for i in tqdm(range(lhs.shape[0])):
        output_matrix.append([])
        for j in range(rhs.shape[1]):
            output_matrix[i].append(FixedHomoFloat(0))
            for k in range(lhs.shape[1]):
                output_matrix[i][j] += lhs[i, k] * rhs[k, j]
    print()

    return np.array(output_matrix)


class MatrixWrapper:
    def __init__(self, mtx):
        self.a = mtx
        self.U = make_array(np.zeros((len(mtx), len(mtx))))
        self.L = make_array(np.eye(len(mtx), len(mtx)))
        self.inv = []
        self.LU_decomposer()

    def LU_decomposer(self):
        j = 0
        while j < len(self.a[0]):
            for i in range(j + 1, len(self.a)):
                pivot = self.a[i][j] / self.a[j][j]
                self.a[i] = self.a[i] - np.array([pivot] * self.a[j].shape[0]) * self.a[j]
                self.L[i][j] = -pivot
            j = j + 1

        for i in range(0, len(self.a)):
            self.U[i] = self.a[i]

    def equation_L(self, b):
        lst = make_array(np.zeros(self.L.shape[0]))
        for i in range(0, self.L.shape[0]):
            for j in range(0, i):
                b[i] = b[i] - self.L[i][j] * lst[j]
            lst[i] = b[i]

        self._b = b

    def equation_U(self):
        lst = make_array(np.zeros(self.U.shape[0]))

        for i in range(self.U.shape[0] - 1, -1, -1):
            for j in range(self.U.shape[0] - 1, -1, -1):
                self._b[i] = self._b[i] - self.U[i][j] * lst[j]

            lst[i] = self._b[i] / self.U[i][i]
            self._b[i] = self._b[i] / self.U[i][i]

        return self._b

    def invert(self):
        size = self.a.shape[0]
        inv = make_array(np.eye(size, size))
        for i in tqdm(range(0, size)):
            self.equation_L(inv[i])
            self.inv += [self.equation_U()]
        self.inv = np.array(self.inv).T
        return np.array(self.inv)


class LinearRegression(BaseEstimator, ClassifierMixin):
    def __init__(self, C=1):
        self.C = C

    def fit(self, X, y=None):
        X_biased = self._transform(X)
        invertible = matmul(X_biased.T, X_biased) + make_array(np.eye(X_biased.shape[1])) * self.C
        print('Got invertible')
        inverted = MatrixWrapper(invertible).invert()
        print('Inverted')
        self._weights = matmul(matmul(inverted, X_biased.T), y.reshape(-1, 1))
        print('Computed weights')

    def predict(self, X, y=None):
        X_biased = self._transform(X)
        return matmul(X_biased, self._weights)

    def _transform(self, X):
        return np.hstack([X, make_array([1] * X.shape[0]).reshape(-1, 1)])
