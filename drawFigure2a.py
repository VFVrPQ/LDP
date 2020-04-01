from protocols.DirectEncoding import DirectEncoding
from Components.Distribution import zipf
from Components.Draw import draw
import math

NUMBEROFAXIS = 7 #### 9
N = 10000 #### 10000

# protocol is class, fixing epsilon
def analytical_eps_DE(protocol, epsilon, n):
    vars = [] # return a list of variances
    for step in range(NUMBEROFAXIS): # 9 values
        d = 2**(2 + step*2)
        x = protocol(d, epsilon)
        x.set_n(n)
        var = x.var_analytical()
        vars.append(math.log10(var)) # log10(var)
    return vars

# zipf distribution, similar to experiments in 14-RAPPOR
def empirical_eps_DE(protocol, epsilon, n):
    vars = []
    for step in range(NUMBEROFAXIS): # 9 values
        d = 2**(2 + step*2)
        x = protocol(d, epsilon) # init
        users = zipf.zipf(1.1, d, n)
        for i in range(len(users)):
            x.PE(users[i])
        x.aggregation() # estimate couterEsti
        
        f = zipf.probList(1.1, d, n)
        var = x.var_empirical(f, n)
        vars.append(math.log10(var)) # log10(var)
    return vars

'''
Need run 10 times.
Temporarily run once.
'''
# Figure 2(a)
def Comparing_empirical_and_analytical_variance_a():
    varslist = [] # return a list of (a list of variances)
    # Analytical DE
    vars = analytical_eps_DE(DirectEncoding, 4, N)
    varslist.append(vars)
    # Empirical DE
    vars = empirical_eps_DE(DirectEncoding, 4, N)
    varslist.append(vars)
    # Draw
    d = [item for item in range(2, (NUMBEROFAXIS+1)*2, 2)] # 2^2, 2^4, ..., 2^18
    draw.lines(d, varslist, ['Analytical DE', 'Empirical DE'], title='Comparing empirical and analytical variance', xlabel='Vary d(log2(x))', ylabel='Var(log10(y))')

if __name__ == "__main__":
    Comparing_empirical_and_analytical_variance_a()