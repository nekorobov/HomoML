import gmpy2
import random
from numpy import polynomial as npp
from numpy.polynomial import polynomial as nppp

'''
Functions for generation of a secret key of the system.
'''
SEED = 213

def nxtodd(num):
    '''
    Simple function to get a next odd number, in order to get
    right amount of complex roots later on

    :param num: int number
    :return: next odd number
    '''
    return num | 1


def complexroot(b):
    '''
    Creates a pair of conjugated complex roots for an upcoming polynomial.
    Real part will lie between [-b;b]; imaginary between [1,b]

    :param b: int number, bordering values for complex roots
    :return: pair of two conjugated complex roots
    '''
    r = random.randint(-1 * b, b)
    i = random.randint(1, b)
    root = complex(r, i)
    return (root, root.conjugate())


def newkey(sec=18, N=2):
    '''
    Generates a secret key with a security parameter sec.
    sec parameter defines amount of complex roots of the private key's polynomial part.

    Result of this function is a key with three fields: polynomial, base, secret encryption number.

    :param sec: security parameter
    :return: secret key object
    '''
    random.seed(SEED)
    r = random.randint(2, N)
    deg = nxtodd(sec)
    sec = (int)((deg - 1) / 2)
    roots = (random.randint(1, r),)
    key = [0 for x in range(deg + 1)]
    for i in range(sec):
        roots += complexroot(r)
    poly = nppp.polyfromroots(roots)
    for d in range(deg + 1):
        key[d] = int(poly[d].real)
    key[0] += r
    coefs = []
    for i in range(len(key)):
        coefs.append(key[i])
    return (coefs, roots[0], r)
