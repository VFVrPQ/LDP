import math
import random

class OUE:
    def __init__(self, d, epsilon, n):
        self.__d = d # input size
        self.__epsilon = epsilon # privacy budget
        self.__p = 1.0 / 2 # probability of pertubation into itself
        self.__q = 1.0 / (math.exp(epsilon) + 1) # probability of pertubation into xxx
        self.__counterPert = d*[0] # count perturbed number
        self.__counterReal = d*[0] # count real number
        self.__counterEsti = d*[0] # ~c(i)
        self.__n = n # the number of users
    
    # Encode(x) = x
    def __encoding(self, x):
        ret = self.__d*[0]
        ret[x-1] = 1
        self.__counterReal[x-1] += 1 # counter
        return ret

    def __perturbing(self, x):
        ret = self.__random_pick(self.__d, x)
        #ret -= 1 # corresponding to index
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
        n = self.__n
        p = self.__p
        q = self.__q     
        for i in range(d):
            self.__counterEsti[i] = (self.__counterPert[i]-n*q)/(p-q)

    # numerical/analytical value of variance
    def var_analytical(self):
        e = math.exp(self.__epsilon)
        if e==1:
            print('var analytical error : e=', 1)
            return -1
        n = self.__n
        return n*4*e/(e-1)/(e-1)

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
            x = random.uniform(0, self.__p+self.__q)
            if x > self.__p : # Pr[0, p] pertubated into itself
                v[i] = 1 - v[i]
        return v