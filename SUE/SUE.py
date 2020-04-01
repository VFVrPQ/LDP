import math
import random

class SUE:
    """Direct Encoding"""
    def __init__(self, d, epsilon, n):
        self.__d = d # input size
        self.__epsilon = epsilon # privacy budget
        self.__p = math.exp(epsilon/2) / (math.exp(epsilon/2)+1) # probability of pertubation into itself
        self.__q = 1.0 / (math.exp(epsilon/2)+1) # probability of pertubation into xxx
        self.__counterPert = d*[0] # count perturbed number
        self.__counterReal = d*[0] # count real number
        self.__n = n # the number of users
    
    # Encode(x) = x
    def __encoding(self, d, x):
        ret = d*[0]
        ret[x-1] = 1
        self.__counterReal[x-1] += 1 # counter
        return ret

    def __perturbing(self, d, x):
        ret = self.__random_pick(d, x)
        #ret -= 1 # corresponding to index
        for i in range(d):
            self.__counterPert[i] += ret[i]
        return ret

    def PE(self, d, x):
        e = self.__encoding(d, x)
        pe = self.__perturbing(d, e)
        return pe

    def aggregation(self):
        self.__counterEsti = self.__d*[0]

        # for convience
        eps = self.__epsilon
        d = self.__d
        n = self.__n
        for i in range(self.__d):
            self.__counterEsti[i] = (self.__counterPert[i]*(math.exp(eps/2)+1)-n)/(math.exp(eps/2)-1)
        return self.__counterReal, self.__counterPert, self.__counterEsti

    # numerical/analytical value of variance
    def var_analytical(self):
        e = math.exp(self.__epsilon/2)
        if e==1:
            print('var analytical error : e=', 1)
            return -1
        d = self.__d
        n = self.__n
        return n*e/(e-1)/(e-1)

    # empirical value of variance
    def var_empirical(self, f):
        d = self.__d
        n = self.__n
        sum = 0.0
        for i in range(d):
            sum += (self.__counterEsti[i]-f[i]*n) ** 2
        return sum/d

    # set n, just for analysis
    def set_n(self, n):
        self.__n = n

    # input number v
    def __random_pick(self, d, v): 
        for i in range(d):
            x = random.uniform(0, 1)
            if x > self.__p: # Pr[0, p] pertubated into itself
                v[i] = 1 - v[i]
        return v