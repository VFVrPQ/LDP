from protocols.LocalHashing import LocalHashing
from Components.Distribution import zipf
from Components.Draw import draw
import math

NUMBEROFAXIS = 10 #### 10
N = 10000 #### 10000

#### begin/BLH ####
# BLH, fixing g=2
def analytical_BLH(protocol, d, n):
    vars = [] # return a list of variances
    for step in range(NUMBEROFAXIS): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon, g=2) # g=2
        x.set_n(n)
        var = x.var_analytical()
        vars.append(math.log10(var)) # log10(var)
    return vars

# zipf distribution, similar to experiments in 14-RAPPOR
# fixing d=2^10
def empirical_BLH(protocol, d, n):
    vars = []
    for step in range(NUMBEROFAXIS): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon, g=2) # init
        users = zipf.zipf(1.1, d, n)
        for i in range(len(users)):
            if i % 1000 == 0:
                print(step, i, "BLH")
            x.PE(users[i])
        x.aggregation() # estimate couterEsti
        
        f = zipf.probList(1.1, d, n)
        var = x.var_empirical(f, n)
        vars.append(math.log10(var))
    return vars
#### end/BLH ####


#### begin/OLH ####
# g = math.exp(epsilon)+1, to the nearst prime
def analytical_OLH(protocol, d, n):
    vars = [] # return a list of variances
    primeList = [3, 3, 5, 7, 13, 23, 37, 53, 89, 149] # according to epsilon=[0.5, 1.0, ..., 5.0]
    for step in range(NUMBEROFAXIS): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon, g=primeList[step])
        x.set_n(n)
        var = x.var_analytical()
        vars.append(math.log10(var)) # log10(var)
    return vars


# zipf distribution, similar to experiments in 14-RAPPOR
# fixing d=2^10
def empirical_OLH(protocol, d, n):
    vars = []
    primeList = [3, 3, 5, 7, 13, 23, 37, 53, 89, 149] # according to epsilon=[0.5, 1.0, ..., 5.0]
    for step in range(NUMBEROFAXIS): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon, g=primeList[step]) # round(math.exp(epsilon)+1)效果不好，要取最近的素数（因为universal hashing！！)
        users = zipf.zipf(1.1, d, n)
        for i in range(len(users)):
            if i % 1000 == 0:
                print(step, i, "OLH")
            x.PE(users[i])
        x.aggregation() # estimate couterEsti
        
        f = zipf.probList(1.1, d, n)
        var = x.var_empirical(f, n)
        vars.append(math.log10(var))
    return vars
#### end/OLH ####

'''
Need run 10 times.
Temporarily run once.
'''
# Figure 2(d)
def Comparing_empirical_and_analytical_variance_d():
    varslist = [] # return a list of (a list of variances)
    # Analytical BLH
    vars = analytical_BLH(LocalHashing, 2**10, N)
    varslist.append(vars)
    # Empirical BLH
    vars = empirical_BLH(LocalHashing, 2**10, N)
    varslist.append(vars)

    # Analytical OLH
    vars = analytical_OLH(LocalHashing, 2**10, N)
    varslist.append(vars)
    # Empirical OLH
    vars = empirical_OLH(LocalHashing, 2**10, N)
    varslist.append(vars)
    
    # Draw
    epss = [0.5+0.5*item for item in range(NUMBEROFAXIS)] # 0.5, 1.0, ..., 5.0
    draw.lines(epss, varslist, ['Analytical BLH', 'Empirical BLH', 'Analytical OLH', 'Empirical OLH'], title='Comparing empirical and analytical variance', xlabel='Vary epsilon(log2(x))', ylabel='Var(log10(y))')

if __name__ == "__main__":
    Comparing_empirical_and_analytical_variance_d()