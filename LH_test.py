from DE.DE import DE
from protocols.LocalHashing import LocalHashing
from Components.Draw import draw
from Components.Distribution import zipf
import math
import numpy as np

# protocol is class
def analytical_BLH(protocol, d, n, g):
    vars = [] # return a list of variances
    for step in range(10): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon, g)
        x.set_n(n)
        vars.append(x.var_analytical())
    return vars

# protocol is class, fixing epsilon
# run very slow, when d is 2^10
def analytical_eps_BLH(protocol, epsilon, n, g):
    vars = [] # return a list of variances
    for step in range(9): #### 9 values
        d = 2**(2 + step*2)
        x = protocol(d, epsilon, g)
        x.set_n(n)
        vars.append(x.var_analytical())
    return vars

# zipf distribution, similar to experiments in 14-RAPPOR
# run very slow, when d is 2^10
def empirical_eps_BLH(protocol, epsilon, n, g):
    vars = []
    for step in range(9): #### 9 values
        d = 2**(2 + step*2)
        x = protocol(d, epsilon, g) # init
        users = zipf.zipf(1.1, d, n)
        for i in range(len(users)):
            if i % 1000 == 0:
                print(step, i, x.get_class_name(), 1)
            x.PE(users[i])
        x.aggregation() # estimate couterEsti
        
        f = zipf.probList(1.1, d)
        vars.append(x.var_empirical(f, n))
    return vars

# g = math.exp(epsilon)+1, to the nearst prime
def analytical_OLH(protocol, d, n):
    vars = [] # return a list of variances
    primeList = [3, 3, 5, 7, 13, 23, 37, 53, 89, 149] # according to epsilon=[0.5, 1.0, ..., 5.0]
    for step in range(10): # 10 values
        epsilon = 0.5 + 0.5 * step
        g = primeList[step]
        x = protocol(d, epsilon, g)
        x.set_n(n)
        vars.append(x.var_analytical())
    return vars

# protocol is class, fixing epsilon
# run very slow, when d is 2^10
def analytical_eps_OLH(protocol, epsilon, n):
    vars = [] # return a list of variances
    g = round(math.exp(epsilon)+1)
    for step in range(9): # 9 values
        d = 2**(2 + step*2)
        x = protocol(d, epsilon, g)
        x.set_n(n)
        vars.append(x.var_analytical())
    return vars

# protocol is class, fixing epsilon
# run very slow, when d is 2^10
def empirical_eps_OLH(protocol, epsilon, n):
    vars = []
    g = 53 # round(math.exp(epsilon)+1)效果不好，要取最近的素数（因为universal hashing！！)
    for step in range(9): #### 9 values
        d = 2**(2 + step*2)
        x = protocol(d, epsilon, g) # init
        users = zipf.zipf(1.1, d, n)
        for i in range(len(users)):
            if i % 1000 == 0:
                print(step, i, x.get_class_name(), 2)
            x.PE(users[i])
        x.aggregation() # estimate couterEsti
        
        f = zipf.probList(1.1, d)
        vars.append(x.var_empirical(f, n))
    return vars

# zipf distribution, similar to experiments in 14-RAPPOR
def empirical(protocol, d, n):
    vars = []
    for step in range(10): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon) # init
        users = zipf.zipf(1.1, d, n)
        for i in range(len(users)):
            x.PE(users[i])
        x.aggregation() # estimate couterEsti
        
        f = zipf.probList(1.1, d)
        vars.append(x.var_empirical(f, n))
    return vars

'''
need run 10 times.
'''
# Figure 1(b)
def numerical_values_of_var2(): 
    varslist = [] # return a list of (a list of variances)
    d=2**10 # 2^10
    # BLH
    vars = analytical_BLH(LocalHashing, d, 10000, 2) 
    for i in range(len(vars)):
        vars[i] = math.log10(vars[i])
    varslist.append(vars)
    # OLH
    vars = analytical_OLH(LocalHashing, d, 10000) # g = math.exp(epsilon)+1
    for i in range(len(vars)):
        vars[i] = math.log10(vars[i])
    varslist.append(vars)

    epss = [0.5+0.5*item for item in range(10)] # 0.5, 1.0, ..., 5.0
    draw.lines(epss, varslist, ['BLH', 'OLH'], ylabel='Var(log10(y))')

# Figure 2(b)
def Comparing_empirical_and_analytical_variance_b():
    n = 10000 ######## 10000
    varslist = [] # return a list of (a list of variances)
    # Analytical BLH
    vars = analytical_eps_BLH(LocalHashing, 4, n, 2)
    for i in range(len(vars)):
        vars[i] = math.log10(vars[i])
    varslist.append(vars)
    # Empirical BLH
    vars = empirical_eps_BLH(LocalHashing, 4, n, 2)
    for i in range(len(vars)): #log10
        vars[i] = math.log10(vars[i])
    varslist.append(vars)

    # Analytical OLH
    vars = analytical_eps_OLH(LocalHashing, 4, n)
    for i in range(len(vars)):
        vars[i] = math.log10(vars[i])
    varslist.append(vars)
    # Empirical OLH
    vars = empirical_eps_OLH(LocalHashing, 4, n)
    for i in range(len(vars)): #log10
        vars[i] = math.log10(vars[i])
    varslist.append(vars)
    # Draw
    d = [item for item in range(2, 20, 2)] # 2^2, 2^4, ..., 2^18
    print(len(d), len(varslist[0]))
    draw.lines(d, varslist, ['Analytical BLH', 'Empirical BLH', 'Analytical OLH', 'Empirical OLH'], title='Comparing empirical and analytical variance', xlabel='Vary d(log2(x))', ylabel='Var(log10(y))')

# Figure 2(c)
def Comparing_empirical_and_analytical_variance2():
    varslist = [] # return a list of (a list of variances)
    # Analytical DE
    vars = analytical(DE, 2**10, 10000)
    for i in range(len(vars)): #log10
        vars[i] = math.log10(vars[i])
    varslist.append(vars)
    #Empirical DE
    vars = empirical(DE, 2**10, 10000)
    for i in range(len(vars)): #log10
        vars[i] = math.log10(vars[i])
    varslist.append(vars)

    # Draw
    eps = [0.5+0.5*item for item in range(10)] # 0.5, 1, ..., 5
    draw.lines(eps, varslist, ['Analytical DE', 'Empirical DE'], title='Comparing empirical and analytical variance', xlabel='Vary epsilon(log2(x))', ylabel='Var(log10(y))')

if __name__ == "__main__":
    #numerical_values_of_var2()
    Comparing_empirical_and_analytical_variance_b()
    #Comparing_empirical_and_analytical_variance2()
