from Components.UniversalHashing import UniversalHashing
import math
import random

class LocalHashing:
    '''
        Local Hashing:including Binary Local Hashing(BLH) and Optimal Local Hashing(OLH),
        the difference is g. BLH's g is 2.
        d: domain, including the values [0, 1, ..., d-1]
        epsilon: privacy budget, >= 0
        g: range, including the values [0, 1, ..., g-1]
    '''
    def __init__(self, d, epsilon, g):
        self.__d = d # input size
        self.__epsilon = epsilon # privacy budget
        self.__g = g
        self.__p = math.exp(epsilon) / (math.exp(epsilon)+g-1) # probability of pertubation into itself
        self.__q = 1.0 / (math.exp(epsilon)+g-1) # probability of pertubation into xxx
        self.__counterPert = d*[0] # count perturbed number
        self.__counterReal = d*[0] # count real number [0,0,...,0]
        self.__n = 0 # the number of users
        
        self.__uh = UniversalHashing(g, d) # universal Hashing
        
    # Encode(v) = <H, x>
    def __encoding(self, v):
        self.__n += 1
        self.__counterReal[v] += 1 # counter
        H, x = self.__uh.hash(v) # v in [0, 1, ..., d-1], x in [0, 1, ..., g-1]
        return H, x

    # Perturb(<H, x>) = <H, y>
    def __perturbing(self, turp): # turple
        H, x = turp
        y = self.__random_pick(x)
        self.__supports(H, y) # counter
        return H, y

    def PE(self, v):
        H, x = self.__encoding(v)
        H, y = self.__perturbing((H, x))
        return H, y

    # aggregation: pure Protocol
    def aggregation(self):
        self.__counterEsti = self.__d*[0]
        n = self.__n 
        pStar = self.__p # p*
        qStar = 1.0 / self.__g # q*
        for i in range(self.__d):
            self.__counterEsti[i] = (self.__counterPert[i]-n*qStar)/(pStar-qStar)

    # pure protocol, numerical/analytical value of variance, 
    # another way to calc is n*( (e-1+g) ** 2)/( (e-1) ** 2)/(g-1)
    def var_analytical(self):
        e = math.exp(self.__epsilon)
        assert e>1, 'var analytical error : e<=1'
        n = self.__n
        pStar = self.__p
        qStar = 1.0 / self.__g
        return n*qStar*(1-qStar)/(pStar-qStar)/(pStar-qStar)


    # empirical value of variance
    # f: list of probability,
    # n: the number 
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

    def get_class_name(self):
        return str(self.__class__.__name__)

    # a set of input values that y "supports"
    # counter
    def __supports(self, H, y):
        for i in range(self.__d): # counter, Support
            temp = self.__uh.calc(H, i)
            if temp == y:
                self.__counterPert[i] += 1 # v in [0, 1, ..., d-1], x in [0, 1, ..., g-1]

    # input number v
    def __random_pick(self, v):
        x = random.uniform(0, 1)
        if x <= self.__p: # Pr[0, p] perturbed into itself
            return v
        # p+(g-1)q = 1, different with DE
        index = int((x-self.__p)/self.__q) # [0, 1, ..., g-2]
        if index >= self.__g-2: # Prevent accidents
            index = self.__g-2
        if index >= x: # skip x
            index += 1
        return index