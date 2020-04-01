from protocols.LocalHashing import LocalHashing
from Components.Distribution import zipf
from Components.Draw import draw
import math

NUMBEROFAXIS = 7 #### 9
N = 10000 #### 10000

#### begin/BLH ####
# protocol is class, fixing epsilon
def analytical_eps_BLH(protocol, epsilon, n):
    vars = [] # return a list of variances
    for step in range(NUMBEROFAXIS):
        d = 2**(2 + step*2)
        x = protocol(d, epsilon, g=2)
        x.set_n(n)
        var = x.var_analytical()
        vars.append(math.log10(var))
    return vars

# zipf distribution, similar to experiments in 14-RAPPOR
# run very slow, when d is 2^10
def empirical_eps_BLH(protocol, epsilon, n):
    vars = []
    for step in range(NUMBEROFAXIS):
        d = 2**(2 + step*2)
        x = protocol(d, epsilon, g=2) # init
        users = zipf.zipf(1.1, d, n)
        for i in range(len(users)):
            if i % 1000 == 0:
                print(step, i, 'BLH')
            x.PE(users[i])
        x.aggregation() # estimate couterEsti
        
        f = zipf.probList(1.1, d, n)
        var = x.var_empirical(f, n)
        vars.append(math.log10(var))
    return vars
#### end/BLH ####


#### begin/OLH ####
# protocol is class, fixing epsilon
def analytical_eps_OLH(protocol, epsilon, n):
    vars = [] # return a list of variances
    g = 53 # round(math.exp(epsilon)+1)效果不好，要取最近的素数（因为universal hashing！！)
    for step in range(NUMBEROFAXIS): # 9 values
        d = 2**(2 + step*2)
        x = protocol(d, epsilon, g)
        x.set_n(n)
        var = x.var_analytical()
        vars.append(math.log10(var))
    return vars

# protocol is class, fixing epsilon
# run very slow, when d is 2^10
def empirical_eps_OLH(protocol, epsilon, n):
    vars = []
    g = 53 # round(math.exp(epsilon)+1)效果不好，要取最近的素数（因为universal hashing！！)
    for step in range(NUMBEROFAXIS): #### 9 values
        d = 2**(2 + step*2)
        x = protocol(d, epsilon, g) # init
        users = zipf.zipf(1.1, d, n)
        for i in range(len(users)):
            if i % 1000 == 0:
                print(step, i, 'OLH')
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
# Figure 2(b)
def Comparing_empirical_and_analytical_variance_b():
    varslist = [] # return a list of (a list of variances)
    # Analytical BLH
    vars = analytical_eps_BLH(LocalHashing, 4, N)
    varslist.append(vars)
    # Empirical BLH
    vars = empirical_eps_BLH(LocalHashing, 4, N)
    varslist.append(vars)

    # Analytical OLH
    vars = analytical_eps_OLH(LocalHashing, 4, N)
    varslist.append(vars)
    # Empirical OLH
    vars = empirical_eps_OLH(LocalHashing, 4, N)
    varslist.append(vars)
    
    # Draw
    d = [item for item in range(2, (NUMBEROFAXIS+1)*2, 2)] # 2^2, 2^4, ..., 2^18
    draw.lines(d, varslist, ['Analytical BLH', 'Empirical BLH', 'Analytical OLH', 'Empirical OLH'], title='Comparing empirical and analytical variance', xlabel='Vary d(log2(x))', ylabel='Var(log10(y))')

if __name__ == "__main__":
    Comparing_empirical_and_analytical_variance_b()