from protocols.DirectEncoding import DirectEncoding
from protocols.LocalHashing import LocalHashing
from Components.Draw import draw
import math

# fixing d, vary epsilon
def analytical_DE(protocol, d, n):
    vars = [] # return a list of variances
    for step in range(10): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon) #!!!
        x.set_n(n)
        var = x.var_analytical()
        vars.append(math.log10(var)) # log10(var)
    return vars

# protocol is class
# BLH, fixing g=2
def analytical_BLH(protocol, d, n):
    vars = [] # return a list of variances
    for step in range(10): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon, g=2) # g=2
        x.set_n(n)
        var = x.var_analytical()
        vars.append(math.log10(var)) # log10(var)
    return vars

# g = math.exp(epsilon)+1, to the nearst prime
def analytical_OLH(protocol, d, n):
    vars = [] # return a list of variances
    primeList = [3, 3, 5, 7, 13, 23, 37, 53, 89, 149] # according to epsilon=[0.5, 1.0, ..., 5.0]
    for step in range(10): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon, g=primeList[step])
        x.set_n(n)
        var = x.var_analytical()
        vars.append(math.log10(var)) # log10(var)
    return vars

'''
Need run 10 times.
Temporarily run once.
'''
# Figure 1(b)
def numerical_values_of_var_b(): 
    varslist = [] # return a list of (a list of variances)
    d=2**10 # 2^10
    # DE
    vars = analytical_DE(DirectEncoding, d, 10000)
    varslist.append(vars)
    # BLH
    vars = analytical_BLH(LocalHashing, d, 10000) 
    varslist.append(vars)
    # OLH
    vars = analytical_OLH(LocalHashing, d, 10000) # g = math.exp(epsilon)+1
    varslist.append(vars)

    # plot
    epss = [0.5+0.5*item for item in range(10)] # 0.5, 1.0, ..., 5.0
    draw.lines(epss, varslist, ['DE','BLH', 'OLH'], ylabel='Var(log10(y))')

if __name__ == "__main__":
    numerical_values_of_var_b()