import math
import random

class DE:
    """Direct Encoding, 
       d:domain, including the values [0, 1, ..., d-1]
    """
    def __init__(self, d, epsilon):
        self.__d = d # input size
        self.__epsilon = epsilon # privacy budget
        self.__p = math.exp(epsilon) / (math.exp(epsilon)+d-1) # probability of pertubation into itself
        self.__q = 1.0 / (math.exp(epsilon)+d-1) # probability of pertubation into xxx
        self.__counterPert = d*[0] # count perturbed number
        self.__counterReal = d*[0] # count real number [0,0,...,0]
        self.__n = 0 # the number of users
    
    # Encode(x) = x
    def __encoding(self, x):
        ret = x
        self.__n += 1
        self.__counterReal[ret] += 1 # counter
        return ret

    def __perturbing(self, x):
        ret = self.__random_pick(x)
        self.__counterPert[ret] += 1
        return ret

    def PE(self, x):
        e = self.__encoding(x)
        pe = self.__perturbing(e)
        return pe

    def aggregation(self):
        self.__counterEsti = self.__d*[0]

        # for convience
        eps = self.__epsilon
        d = self.__d
        n = self.__n
        for i in range(self.__d):
            self.__counterEsti[i] = (self.__counterPert[i]*(math.exp(eps)+d-1)-n)/(math.exp(eps)-1)
        #return self.__counterReal, self.__counterPert, self.__counterEsti

    # numerical/analytical value of variance
    def var_analytical(self):
        e = math.exp(self.__epsilon)
        if e==1:
            print('var analytical error : e=', 1)
            return -1
        d = self.__d
        n = self.__n
        return n*(d-2+e)/(e-1)/(e-1)

    # empirical value of variance
    # f: list of probability; n : the number 
    def var_empirical(self, f, n):
        d = self.__d
        sum = 0.0
        for i in range(d):
            sum += (self.__counterEsti[i] - 1.0*f[i]*n) ** 2
        return sum / d

    # set n, just for analysis
    def set_n(self, n):
        self.__n = n

    def get_n(self):
        return self.__n

    # input number v
    def __random_pick(self, v):
        x = random.uniform(0, 1)
        if x <= self.__p: # Pr[0, p] perturbed into itself
            return v
        # p+(d-1)q = 1
        index = int((x-self.__p)/self.__q) # [0, 1, ..., d-2]
        if index >= self.__d-2: # Prevent accidents
            index = self.__d-2
        if index >= x: # skip x
            index += 1
        return index
        '''
        # Below method is too slow
        # except x
        cumulative_probability = self.__p
        item = 0 #[0, 1, ..., d-1]
        if item == v:
            item += 1
        item_probabitity = self.__q

        while 1:
            #print(self.__p, self.__q, item, cumulative_probability)
            cumulative_probability += item_probabitity
            if x <= cumulative_probability:
                return item
            item += 1
            if item == v:
                item += 1
            if item >= self.__d: # bound
                return self.__d-1
        '''