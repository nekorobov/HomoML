'''
Functions for computing the resulting lamda-functions on another end of cyphering.
Mostly for testing and visibility.
'''


def add(encr1, encr2, *args):
    '''
    Computes the sum of all functions in parameters.
    :param encr1: lambda function
    :param encr2: lambda function
    :param args: additional lambda functions
    :return: lambda function, sum of parameters
    '''
    if (args):
        return lambda x: encr1(x) + (add(encr2, *args))(x)
    else:
        return lambda x: encr1(x) + encr2(x)


def sub(encr1, encr2):
    '''
    Substracts encr2 function from encr1.
    :param encr1: lambda function
    :param encr2: lambda function
    :return: lambda function, result of substracrion
    '''
    return lambda x: encr1(x) - encr2(x)


def mul(encr1, encr2, *args):
    '''
    Computes the product of all functions in parameters.
    :param encr1: lambda function
    :param encr2: lambda function
    :param args: additional lambda functions
    :return: lambda function, product of parameters
    '''
    if (args):
        return lambda x: encr1(x) * (multi(encr2, *args))(x)
    else:
        return lambda x: encr1(x) * encr2(x)


def div(encr1, encr2):
    '''
    Divides encr1 function by encr2.
    :param encr1: lambda function
    :param encr2: lambda function, non-zero due to encryption rules and methods
    :return: lambda function, result of division
    '''
    return lambda x: encr1(x) / encr2(x)
