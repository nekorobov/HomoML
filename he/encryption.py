import gmpy2
import numpy as np
from numpy import polynomial as npp
from numpy.polynomial import polynomial as nppp
import string

'''
Functions for encrypting.
'''

def inttopoly(num, base):
    '''
    Converts an int number into a polynomial, representing num in another numeral system.

    :param num: integer number to convert.
    :param base: base number of the numeral system.
    :return: numpy.polynomial.Polynomial object, representing integer num in the numeral system with base number base.
    '''

    coeffs = []
    sign = 1
    if num < 0:
        sign = -1
        num *= -1
    new_num = gmpy2.digits(num, base)
    for digit in new_num:
        if not digit.isdigit():
            d = ord(digit.lower()) - ord('a') + 10
        else:
            d = int(digit)
        coeffs = [sign * d] + coeffs
    return npp.Polynomial(coeffs)


def isrealpoly(poly):
    '''
    Checks if polynomial's coefficients are real.

    :param poly: numpy.polynomial.Polynomial object
    :return: 1 if polynomial's coefficients are real, 0 if not
    '''
    for coef in poly:
        if coef.imag != 0:
            return 0
    return 1


def poly(coeffs):
    '''
    Builds a lambda function from a set of coefficients

    :param coeffs: array of int coeeficients of the polynomial
    :return: lambda function representing this polynomial
    '''
    def calc(x):
        '''
        :param x: variable of polynomial
        :return: function of polynomial
        '''
        result = 0
        for i, c in enumerate(coeffs):
            result += c * (x ** i)
        return result

    return calc


def rebase(number, base):
    '''
    Transforms an int number into another numbering system

    :param number: int number
    :param base:  base of a numbering system, int
    :return:
    '''
    return inttopoly(number, base)


def rebase_all(numbers, base):
    '''

    :param numbers: iterable, int numbers
    :param base: base of a numbering system, int
    :return:
    '''
    return [rebase(num, base) for num in numbers]


def encrypttopoly(number, key):
    '''
    Encrypts a number with a given key.

    :param number: int number to encrypt
    :param key: secret key of a system
    :return:polynomial
    '''
    rebased = rebase(number, key[2])
    poly_num = poly(rebased.coef)
    key_poly = poly(key[0])
    return lambda x: poly_num(key_poly(x))
