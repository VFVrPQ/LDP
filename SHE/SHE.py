import math
import random
from Components.Distribution import laplace

class SHE:
    def __init__(self, d, epsilon, n):
        self.__d = d # input size
        self.__epsilon = epsilon # privacy budget
        self.__counterPert = d*[0] # count perturbed number
        self.__counterReal = d*[0] # count real number
        self.__counterEsti = d*[0] # ~c(i)
        self.__n = n # the number of users
    
    # Encode(x) = x
    def __encoding(self, x):
        ret = self.__d*[0.0]
        ret[x-1] = 1.0
        self.__counterReal[x-1] += 1 # counter
        return ret

    def __perturbing(self, x):
        ret = self.__random_pick(x)
        for i in range(self.__d):
            self.__counterPert[i] += ret[i]
        return ret

    def PE(self, x):
        e = self.__encoding(x)
        pe = self.__perturbing(e)
        return pe

    def aggregation(self):
        # for convience
        d = self.__d
        for i in range(d):
            self.__counterEsti[i] = self.__counterPert[i]
        if d == 4 :
            print(self.__counterEsti,self.__counterReal,self.__counterPert)    

    # numerical/analytical value of variance
    def var_analytical(self):
        e = self.__epsilon
        if e==0:
            print('var analytical error : e=', 0)
            return -1
        n = self.__n
        return n*8/e/e

    # empirical value of variance
    def var_empirical(self, f):
        d = self.__d
        n = self.__n
        sum = 0.0
        for i in range(d):
            sum += (self.__counterEsti[i] - f[i]*n) ** 2
        return sum/d

    # input number v
    def __random_pick(self, v):
        d = self.__d
        for i in range(d) :
            v[i] = v[i] + laplace.laplace(2/self.__epsilon, 1)
        return v