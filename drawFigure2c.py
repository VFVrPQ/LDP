from protocols.DirectEncoding import DirectEncoding
from Components.Distribution import zipf
from Components.Draw import draw
import math

NUMBEROFAXIS = 10 #### 9
N = 10000 #### 10000

# fixing d, vary epsilon
## copy from drawFigure1a
def analytical_DE(protocol, d, n):
    vars = [] # return a list of variances
    for step in range(NUMBEROFAXIS):
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon)
        x.set_n(n)
        var = x.var_analytical()
        vars.append(math.log10(var)) # log10(var)
    return vars

# zipf distribution, similar to experiments in 14-RAPPOR
def empirical_DE(protocol, d, n):
    vars = []
    for step in range(NUMBEROFAXIS): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon) # init
        users = zipf.zipf(1.1, d, n)
        for i in range(len(users)):
            x.PE(users[i])
        x.aggregation() # estimate couterEsti
        
        f = zipf.probList(1.1, d, n)
        var = x.var_empirical(f, n)
        vars.append(math.log10(var))
    return vars

'''
Need run 10 times.
Temporarily run once.
'''
# Figure 2(c)
def Comparing_empirical_and_analytical_variance_c():
    varslist = [] # return a list of (a list of variances)
    # Analytical DE
    vars = analytical_DE(DirectEncoding, 2**10, N)
    varslist.append(vars)
    # Empirical DE
    vars = empirical_DE(DirectEncoding, 2**10, N)
    varslist.append(vars)

    # Draw
    eps = [0.5+0.5*item for item in range(NUMBEROFAXIS)] # 0.5, 1, ..., 5
    draw.lines(eps, varslist, ['Analytical DE', 'Empirical DE'], title='Comparing empirical and analytical variance', xlabel='Vary epsilon(log2(x))', ylabel='Var(log10(y))')

if __name__ == "__main__":
    Comparing_empirical_and_analytical_variance_c()