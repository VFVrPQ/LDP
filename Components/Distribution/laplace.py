'''
reference:https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.random.laplace.html
'''
import numpy as np

def laplace(scale, size):
    '''
        scale : lambda
        size: int or tuple of ints, optional
    '''
    return np.random.laplace(0.0, scale, size)

if __name__ == '__main__':
    print(laplace(200, 10))