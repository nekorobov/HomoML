import numpy as np

import he.key as hek
import he.encryption as hee
import he.decryption as hed
import he.computation as hec


def is_builtin(obj):
	return True


class FixedHomoFloat:
	def __init__(self, value, k=0, N=2, sec=18, key=None, M=None, max_k=256):
		if k >= max_k or k < 0:
			raise ValueError('Incorrect k')

		self.max_k = max_k
		self.k = k
		self.__value = value
		if key is None:
			self.__key = hek.newkey(sec=sec, N=N)
		else:
			self.__key = key
		val = int(value * (10 ** self.k))
		if M is None:
			self.M = hee.encrypttopoly(val, self.__key)
		else:
			self.M = M

	def __rmul__(self, other):
		if is_builtin(other):
			if self.k * 2 < self.max_k and self.k * 2 >= 0:
				M1 = hee.encrypttopoly(int(other * (10 ** self.k)), self.__key)
				M1 = hec.mul(self.M, M1)
				k1 = self.k * 2
			else:
				raise ValueError('Wrong k: {}'.format(self.k))
		else:
			raise TypeError('Unknown type for multiplication')
		return FixedHomoFloat(0, k=k1, M=M1, key=self.__key)

	def __mul__(self, other):
		if isinstance(other, FixedHomoFloat):
			if self.k + other.k < self.max_k and self.k + other.k >= 0:
				M1 = hec.mul(self.M, other.M)
				k1 = self.k + other.k
			else:
				raise ValueError('Too big k')
		elif is_builtin(other):
			if self.k * 2 < self.max_k and self.k * 2 >= 0:
				M1 = hee.encrypttopoly(int(other * (10 ** self.k)), self.__key)
				M1 = hec.mul(self.M, M1)
				k1 = self.k * 2
			else:
				raise ValueError('Wrong k')
		else:
			raise TypeError('Unknown type for multiplication')
		return FixedHomoFloat(0, k=k1, M=M1, key=self.__key)

	def __rtruediv__(self, other):
		if is_builtin(other):
			M1 = hee.encrypttopoly(int(other * (10 ** self.k)), self.__key)
			M1 = hec.div(M1, self.M)
			k1 = 0
		else:
			raise TypeError('Unknown type for division')
		return FixedHomoFloat(0, k=0, M=M1, key=self.__key)

	def __truediv__(self, other):
		if isinstance(other, FixedHomoFloat):
			if self.k - other.k < self.max_k and self.k - other.k >= 0:
				k1 = self.k - other.k
				M1 = hec.div(self.M, other.M)
			else:
				raise ValueError('Wrong k')
		elif is_builtin(other):
			M1 = hee.encrypttopoly(int(other * (10 ** self.k)), self.__key)
			M1 = hec.div(self.M, M1)
			k1 = 0
		else:
			raise TypeError('Unknown type for division')
		return FixedHomoFloat(0, k=k1, M=M1, key=self.__key)

	def __radd__(self, other):
		if is_builtin(other):
			M1 = hee.encrypttopoly(int(other * (10 ** self.k)), self.__key)
			M1 = hec.add(self.M, M1)
			k1 = self.k
		else:
			raise TypeError('Unknown type for addition')
		return FixedHomoFloat(0, k=k1, M=M1, key=self.__key)

	def __add__(self, other):
		if isinstance(other, FixedHomoFloat):
			diff_k = self.k - other.k
			neg = False
			if diff_k < 0:
				neg = True
				diff_k *= -1

			M1 = hee.encrypttopoly(int((10 ** diff_k)), self.__key)
			if not neg:
				M1 = hec.mul(other.M, M1)
				M1 = hec.add(M1, self.M)
				k1 = self.k
			else:
				M1 = hec.mul(self.M, M1)
				if self.k + diff_k < self.max_k and self.k + diff_k >= 0:
					k1 = self.k + diff_k
					M1 = hec.add(M1, other.M)
				else:
					raise ValueError('Wrong k')
		elif is_builtin(other):
			M1 = hee.encrypttopoly(int(other * (10 ** self.k)), self.__key)
			M1 = hec.add(self.M, M1)
			k1 = self.k
		else:
			raise TypeError('Unknown type for addition')
		return FixedHomoFloat(0, k=k1, M=M1, key=self.__key)

	def __neg__(self):
		return -1 * self

	def __rsub__(self, other):
		if is_builtin(other):
			M1 = hee.encrypttopoly(int(other * (10 ** self.k)), self.__key)
			M1 = hec.sub(M1, self.M)
			k1 = self.k
		else:
			raise TypeError('Unknown type for substraction')
		return FixedHomoFloat(0, k=k1, M=M1, key=self.__key)

	def __sub__(self, other):
		if isinstance(other, FixedHomoFloat):
			diff_k = self.k - other.k
			neg = False
			if diff_k < 0:
				neg = True
				diff_k *= -1

			M1 = hee.encrypttopoly(int((10 ** diff_k)), self.__key)
			if not neg:
				M1 = hec.mul(other.M, M1)
				M1 = hec.sub(self.M, M1)
				k1 = self.k
			else:
				M1 = hec.mul(self.M, M1)
				if self.k + diff_k < self.max_k and self.k + diff_k >= 0:
					M1 = hec.sub(M1, other.M)
					k1 = self.k + diff_k
				else:
					raise ValueError('Wrong k')
		elif is_builtin(other):
			M1 = hee.encrypttopoly(int(other * (10 ** self.k)), self.__key)
			M1 = hec.sub(self.M, M1)
			k1 = self.k
		else:
			raise TypeError('Unknown type for substraction')
		return FixedHomoFloat(0, k=k1, M=M1, key=self.__key)

	# On client side functions
	def __le__(self, other):
		if isinstance(other, FixedHomoFloat):
			diff_k = self.k - other.k
			neg = False
			if diff_k < 0:
				neg = True
				diff_k *= -1

			M1 = hee.encrypttopoly(int((10 ** diff_k)), self.__key)
			if not neg:
				M1 = hec.mul(other.M, M1)
				m1 = hed.decrypt(self.M, self.__key)
				m2 = hed.decrypt(M1, self.__key)
			else:
				M1 = hec.mul(self.M, M1)
				m1 = hed.decrypt(M1, self.__key)
				m2 = hed.decrypt(other.M, self.__key)
			return m1 <= m2
		else:
			raise TypeError('Unknown type for comparing')

	def __lt__(self, other):
		if isinstance(other, FixedHomoFloat):
			diff_k = self.k - other.k
			neg = False
			if diff_k < 0:
				neg = True
				diff_k *= -1

			M1 = hee.encrypttopoly(int((10 ** diff_k)), self.__key)
			if not neg:
				M1 = hec.mul(other.M, M1)
				m1 = hed.decrypt(self.M, self.__key)
				m2 = hed.decrypt(M1, self.__key)
			else:
				M1 = hec.mul(self.M, M1)
				m1 = hed.decrypt(M1, self.__key)
				m2 = hed.decrypt(other.M, self.__key)
			return m1 < m2
		else:
			raise TypeError('Unknown type for comparing')

	def __ge__(self, other):
		if isinstance(other, FixedHomoFloat):
			diff_k = self.k - other.k
			neg = False
			if diff_k < 0:
				neg = True
				diff_k *= -1

			M1 = hee.encrypttopoly(int((10 ** diff_k)), self.__key)
			if not neg:
				M1 = hec.mul(other.M, M1)
				m1 = hed.decrypt(self.M, self.__key)
				m2 = hed.decrypt(M1, self.__key)
			else:
				M1 = hec.mul(self.M, M1)
				m1 = hed.decrypt(M1, self.__key)
				m2 = hed.decrypt(other.M, self.__key)
			return m1 >= m2
		else:
			raise TypeError('Unknown type for comparing')

	def __gt__(self, other):
		if isinstance(other, FixedHomoFloat):
			diff_k = self.k - other.k
			neg = False
			if diff_k < 0:
				neg = True
				diff_k *= -1

			M1 = hee.encrypttopoly(int((10 ** diff_k)), self.__key)
			if not neg:
				M1 = hec.mul(other.M, M1)
				m1 = hed.decrypt(self.M, self.__key)
				m2 = hed.decrypt(M1, self.__key)
			else:
				M1 = hec.mul(self.M, M1)
				m1 = hed.decrypt(M1, self.__key)
				m2 = hed.decrypt(other.M, self.__key)
			return m1 > m2
		else:
			raise TypeError('Unknown type for comparing')

	def __eq__(self, other):
		if isinstance(other, FixedHomoFloat):
			diff_k = self.k - other.k
			neg = False
			if diff_k < 0:
				neg = True
				diff_k *= -1

			M1 = hee.encrypttopoly(int((10 ** diff_k)), self.__key)
			if not neg:
				M1 = hec.mul(other.M, M1)
				m1 = hed.decrypt(self.M, self.__key)
				m2 = hed.decrypt(M1, self.__key)
			else:
				M1 = hec.mul(self.M, M1)
				m1 = hed.decrypt(M1, self.__key)
				m2 = hed.decrypt(other.M, self.__key)
			return m1 == m2
		else:
			raise TypeError('Unknown type for comparing')

	def __ne__(self, other):
		if isinstance(other, FixedHomoFloat):
			diff_k = self.k - other.k
			neg = False
			if diff_k < 0:
				neg = True
				diff_k *= -1

			M1 = hee.encrypttopoly(int((10 ** diff_k)), self.__key)
			if not neg:
				M1 = hec.mul(other.M, M1)
				m1 = hed.decrypt(self.M, self.__key)
				m2 = hed.decrypt(M1, self.__key)
			else:
				M1 = hec.mul(self.M, M1)
				m1 = hed.decrypt(M1, self.__key)
				m2 = hed.decrypt(other.M, self.__key)
			return m1 != m2
		else:
			raise TypeError('Unknown type for comparing')

	def get_value(self):
		return hed.decrypt(self.M, self.__key) * (10 ** (-self.k))

	def __str__(self):
		return str(self.get_value())

	def __repr__(self):
		return self.__str__()


def make_array(lst):
	return np.vectorize(FixedHomoFloat)(np.array(lst))
