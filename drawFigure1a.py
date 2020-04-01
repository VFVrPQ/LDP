from protocols.DirectEncoding import DirectEncoding
from Components.Draw import draw
import math

# fixing d, vary epsilon
def analytical_DE(protocol, d, n):
    vars = [] # return a list of variances
    for step in range(10): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon)
        x.set_n(n)
        var = x.var_analytical()
        vars.append(math.log10(var)) # log10(var)
    return vars

'''
Need run 10 times.
Temporarily run once.
'''
# Figure 1(a)
def numerical_values_of_var_a(): 
    varslist = [] # return a list of (a list of variances)
    for d in [2, 4, 16, 128, 2048]:
        vars = analytical_DE(DirectEncoding, d, 10000)
        varslist.append(vars)
    # plot
    epss = [0.5+0.5*item for item in range(10)] # 0.5, 1.0, ..., 5.0
    draw.lines(epss, varslist, ['DE(d=2)', 'DE(d=4)', 'DE(d=16)', 'DE(d=128)', 'DE(d=2048)'], ylabel='Var(log10(y))')

if __name__ == "__main__":
    numerical_values_of_var_a()