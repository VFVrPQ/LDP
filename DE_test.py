from DE.DE import DE
from Components.Draw import draw
from Components.Distribution import zipf
import math
import numpy as np

# protocol is class
def analytical(protocol, d, n):
    vars = [] # return a list of variances
    for step in range(10): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon)
        x.set_n(n)
        vars.append(x.var_analytical())
    return vars

# protocol is class, fixing epsilon
def analytical_eps(protocol, epsilon, n):
    vars = [] # return a list of variances
    for step in range(9): # 9 values
        d = 2**(2 + step*2)
        x = protocol(d, epsilon)
        x.set_n(n)
        vars.append(x.var_analytical())
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

# zipf distribution, similar to experiments in 14-RAPPOR
def empirical_eps(protocol, epsilon, n):
    vars = []
    for step in range(9): # 9 values
        d = 2**(2 + step*2)
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
# Figure 1(a)
def numerical_values_of_var1(): 
    varslist = [] # return a list of (a list of variances)
    for d in [2, 4, 16, 128, 2048]:
        vars = analytical(DE, d, 10000)
        for i in range(len(vars)):
            vars[i] = math.log(vars[i]) / math.log(10)
        varslist.append(vars)
    epss = [0.5+0.5*item for item in range(10)] # 0.5, 1.0, ..., 5.0
    draw.lines(epss, varslist, ['DE(d=2)', 'DE(d=4)', 'DE(d=16)', 'DE(d=128)', 'DE(d=2048)'], ylabel='Var(log10(y))')

# Figure 1(b)
def numerical_values_of_var2(): 
    varslist = [] # return a list of (a list of variances)
    d=2**10 # 2^10
    vars = analytical(DE, d, 10000)
    for i in range(len(vars)):
        vars[i] = math.log(vars[i]) / math.log(10)
    varslist.append(vars)
    epss = [0.5+0.5*item for item in range(10)] # 0.5, 1.0, ..., 5.0
    draw.lines(epss, varslist, ['DE'], ylabel='Var(log10(y))')

# Figure 2(a)
def Comparing_empirical_and_analytical_variance1():
    varslist = [] # return a list of (a list of variances)
    # Analytical DE
    vars = analytical_eps(DE, 4, 10000)
    for i in range(len(vars)): #log10
        vars[i] = math.log(vars[i]) / math.log(10)
    varslist.append(vars)
    # Empirical DE
    vars = empirical_eps(DE, 4, 10000)
    for i in range(len(vars)): #log10
        vars[i] = math.log(vars[i]) / math.log(10)
    varslist.append(vars)

    # Draw
    d = [item for item in range(2, 20, 2)] # 2^2, 2^4, ..., 2^18
    draw.lines(d, varslist, ['Analytical DE', 'Empirical DE'], title='Comparing empirical and analytical variance', xlabel='Vary d(log2(x))', ylabel='Var(log10(y))')

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
    #numerical_values_of_var1()
    #numerical_values_of_var2()
    Comparing_empirical_and_analytical_variance1()
    #Comparing_empirical_and_analytical_variance2()