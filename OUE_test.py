from OUE.OUE import OUE
from Components.Draw import draw
from Components.Distribution import zipf
import math
import random

# protocol is class
def analytical(protocol, d, n):
    vars = [] # return a list of variances
    for step in range(10): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon, n)
        #x.set_n(n)
        vars.append(x.var_analytical())
    return vars

# protocol is class, fixing epsilon
def analytical_eps(protocol, epsilon, n):
    vars = [] # return a list of variances
    for step in range(7): # 9 values
        d = 2**(2 + step*2)
        x = protocol(d, epsilon, n)
        #x.set_n(n)
        vars.append(x.var_analytical())
    return vars

def empirical_eps(protocol, epsilon, n):
    vars = []
    for step in range(7): # 9 values
        d = 2**(2 + step*2)
        #f = []
        x = protocol(d, epsilon, n)
        users = zipf.zipf(1.1, d, n)
        for i in range(n): # random PE
            if i%1000 == 0:
                print(i,step)
            #m = random.randint(1,d)
            #x.PE(m)
            x.PE(users[i]+1)
            
        f = zipf.probList(1.1, d, n)
        #for i in range(d):
        #    f.append(1.0/d)
        #print(f)
        x.aggregation()
        vars.append(x.var_empirical(f))
    return vars

# like Figure 1(b)
def numerical_values_of_var2(): 
    varslist = [] # return a list of (a list of variances)
    d=2**10 # 2^10
    vars = analytical(OUE, d, 10000)
    for i in range(len(vars)):
        vars[i] = math.log(vars[i]) / math.log(10)
    varslist.append(vars)
    epss = [0.5+0.5*item for item in range(10)] # 0.5, 1.0, ..., 5.0
    draw.lines(epss, varslist, ['OUE'], ylabel='Var(log10(y))')

# Figure 2(a)
def Comparing_empirical_and_analytical_variance1():
    varslist = [] # return a list of (a list of variances)
    # Analytical DE
    vars = analytical_eps(OUE, 4, 10000)
    for i in range(len(vars)): #log10
        vars[i] = math.log(vars[i]) / math.log(10)
    varslist.append(vars)
    # Empirical DE
    
    vars = empirical_eps(OUE, 4, 10000)
    for i in range(len(vars)): #log10
        vars[i] = math.log(vars[i]) / math.log(10)
    varslist.append(vars)
    
    # Draw
    d = [item for item in range(2, 16, 2)] # 2^2, 2^4, ..., 2^18
    draw.lines(d, varslist, ['Analytical OUE', 'Empirical OUE'], xlabel='Vary d(log2(d))', ylabel='Vary n(log10(n))')

#numerical_values_of_var2()
Comparing_empirical_and_analytical_variance1()