'''
Function for decrypting.
'''


def decrypt(func, key):
    '''

    :param func: lambda function obtained from the server
    :param key: keys
    :return: decrypted value
    '''
    return func(key[2])
