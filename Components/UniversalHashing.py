'''
references: http://cs-www.bu.edu/faculty/homer/537/talks/SarahAdelBargal_UniversalHashingnotes.pdf
'''
import math
import random
class UniversalHashing:
    '''
        g: a prime
        d: domain, [0, 1, ..., d-1]
        len: The maximum number of digits in g Base
        v: an input value in [0, 1, ..., d-1] 
        hash function: H_a(k) = (a(0)*k(0)+a(1)*k(1)+...+a(len-1)*k(len-1)) % g
    '''
    def __init__(self, g, d):
        self.__g = g
        assert g>=2, 'g is less than 2'
        assert self.__isPrime(g), 'g is not a prime'

        self.__d = d
        self.__len = math.ceil( math.log(d) / math.log(g)) # g进制下，最大的位数
        self.__a = self.__len*[0] # initial length
    
    # v is an input value in [0, 1, ..., d-1] 
    def hash(self, v):
        self.__randomness() # regenerate a, select H
        out = self.calc(self.__a, v)
        return self.__a, out

    # calc H_a(k) = (a(0)*k(0)+a(1)*k(1)+...+a(len-1)*k(len-1)) % g
    def calc(self, a, v):
        assert len(a)==self.__len, 'len(a)!=self.__len'
        k = self.__toBitList(v)
        out = 0
        for i in range(self.__len):
            out = (out + a[i]*k[i]) % self.__g
        return out

    def __randomness(self):
        # generate a
        for i in range(self.__len):
            self.__a[i] = random.randint(0, self.__g-1)

    def __toBitList(self, v):
        assert v>=0, 'v<0'
        if v == 0:
            return self.__len * [0]
        bitList = self.__len * [0]
        for i in range(self.__len):
            bitList[i] = v%self.__g
            v = int(v/self.__g)
        return bitList
    
    def __isPrime(self, v):
        if v<=1:
            return False
        for i in range(2, int(math.sqrt(v))+1, 1):
            if v%i==0:
                return False
        return True

# for test
if __name__ == "__main__":
    TIMES = 10
    g = 29 # prime
    d = 16 # domain
    uhash = UniversalHashing(g, d)
    H = g * [0]
    for i in range(TIMES): # random TIMES to verify
        x = random.randint(0, d-1)
        _, out = uhash.hash(x)
        H[out] += 1
    for i in range(g):
        print(i, H[i])

    