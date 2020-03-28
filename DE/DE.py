import math
import random

class DE:
    """Direct Encoding"""
    def __init__(self, d, epsilon):
        self.__d = d # input size
        self.__epsilon = epsilon # privacy budget
        self.__p = math.exp(epsilon) / (math.exp(epsilon)+d-1) # probability of pertubation into itself
        self.__q = 1.0 / (math.exp(epsilon)+d-1) # probability of pertubation into xxx
        self.__counterNew = d*[0] # count perturbed number
        self.__counterReal = d*[0] # count real number
        self.__n = 0 # the number of users
    
    # Encode(x) = x
    def __encoding(self, x):
        ret = x
        self.__n += 1
        self.__counterReal[ret] += 1 # counter
        return ret

    def __perturbing(self, x):
        ret = self.__random_pick(x)
        ret -= 1 # corresponding to index
        self.__counterNew[ret] += 1
        return ret

    def PE(self, x):
        e = self.__encoding(x)
        pe = self.__perturbing(e)
        return pe

    def aggregation(self):
        estimate_c = self.__d*[0]

        # for convience
        eps = self.__epsilon
        d = self.__d
        n = self.__n
        for i in range(self.__d):
            estimate_c[i] = (self.__counterNew[i]*(math.exp(eps)+d-1)-n)/(math.exp(eps)-1)
        return self.__counterReal, self.__counterNew, estimate_c

    # input number v
    def __random_pick(self, v): 
        x = random.uniform(0, 1)
        if x <= self.__p: # Pr[0, p] pertubated into itself
            return v
        # except x
        cumulative_probability = self.__p
        item = 1
        if item == v:
            item += 1
        item_probabitity = self.__q

        while 1:
            cumulative_probability += item_probabitity
            if x <= cumulative_probability:
                return item
            item += 1
            if item == v:
                item +=x
            if item > self.__d: # bound
                return self.__d