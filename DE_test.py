from DE.DE import DE
from Components.Draw import draw
import math

def empirical():
    TIMES = 1000
    d = 2
    epsilon = 3
    x = DE(d, epsilon)

    real = d*[0]
    pert = d*[0]
    esti = d*[0]

    # Encoding & perturbing
    for num in range(TIMES):
        for i in range(d):
            _ = x.PE(i)
    # aggregation
    r, p, e = x.aggregation()
    for j in range(d):
        real[j] += r[j]
        pert[j] += p[j]
        esti[j] += e[j]

    print('value, realNum, perturbingNum, estimationNum')
    for i in range(d):
        print('%d: ' %i, real[i], pert[i], esti[i])

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

def empirical_eps(protocol, epislon, n):
    vars = []
    for step in range(9): # 9 values
        d = 2**(2 + step*2)
        x = protocol(d, epislon)
        for i in range(n): # random PE
            
# like Figure 1(a)
def numerical_values_of_var1(): 
    varslist = [] # return a list of (a list of variances)
    for d in [2, 4, 16, 128, 2048]:
        vars = analytical(DE, d, 10000)
        for i in range(len(vars)):
            vars[i] = math.log(vars[i]) / math.log(10)
        varslist.append(vars)
    epss = [0.5+0.5*item for item in range(10)] # 0.5, 1.0, ..., 5.0
    draw.lines(epss, varslist, ['DE(d=2)', 'DE(d=4)', 'DE(d=16)', 'DE(d=128)', 'DE(d=2048)'], ylabel='Var(log10(y))')

# like Figure 1(b)
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

    # Draw
    d = [item for item in range(2, 20, 2)] # 2^2, 2^4, ..., 2^18
    draw.lines(d, varslist, ['Analytical DE'], xlabel='Vary epislon(log2(x))', ylabel='Var(log10(y))')

#numerical_values_of_var1()
#numerical_values_of_var2()
Comparing_empirical_and_analytical_variance1()