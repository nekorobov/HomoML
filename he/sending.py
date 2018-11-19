import dill
import pickle

'''
Functions for sending an encrypted message to a server.
'''

def restobytes(func):
    '''
    Serialization of the encrypted numbers
    :param func:  function to serialize (int or lambda function)
    :return: byte representation array of ints or lambda function
    '''
    return dill.dumps(func)

def get_result(res):
    '''
    Deserialization of the result
    :param res: resulting byte representation array of ints or lambda function
    :return: array of ints or lambda function
    '''
    return dill.loads(res)