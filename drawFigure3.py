from protocols.LocalHashing import LocalHashing
from Components.Draw import draw
import math

# 从文件（仅包含整数和空格）中读取所有的整数。
def readIntList(filename):
    numbers = []
    with open(filename, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.split()
            #print(line)
            for i in line:
                numbers.append(int(i))
    return numbers


#### begin/BLH ####

NUMBEROFAXIS = 10 #### 10
KK = 30
# BLH, fixing g=2
# fixing d=2^10
def empirical_BLH(protocol, d, numbers):
    vars = []
    for step in range(NUMBEROFAXIS): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon, g=2) # init
        for i in range(len(numbers)):
            if i % 100 == 0: print(step, i, "BLH") #log
            x.PE(numbers[i])
        x.aggregation() # estimate couterEsti
        
        var = x.var_empirical_top_k(KK)
        vars.append(math.log10(var))
    return vars
#### end/BLH ####


#### begin/OLH ####
# zipf distribution, similar to experiments in 14-RAPPOR
# fixing d=2^10
primeList = [3, 3, 5, 7, 13, 23, 37, 53, 89, 149] # according to epsilon=[0.5, 1.0, ..., 5.0]
def empirical_OLH(protocol, d, numbers):
    vars = []
    for step in range(NUMBEROFAXIS): # 10 values
        epsilon = 0.5 + 0.5 * step
        x = protocol(d, epsilon, g = primeList[step]) # g=round(math.exp(epsilon)+1)效果不好，要取最近的素数（因为universal hashing！！)
        for i in range(len(numbers)):
            if i % 100 == 0:
                print(step, i, "OLH")
            x.PE(numbers[i])
        x.aggregation() # estimate couterEsti
        
        var = x.var_empirical_top_k(KK)
        vars.append(math.log10(var))
    return vars
#### end/OLH ####

# Figure 3
def drawFigure3():
    numbers = readIntList('./data/kosarak.dat')
    numbers = numbers[0:1000] ###### too much values, so cut off 
    maxnum = max(numbers)
    totnum = len(numbers)
    print('maxnum, totnum: ', maxnum, totnum)

    varslist = []
    # Empirical BLH
    vars = empirical_BLH(LocalHashing, d=maxnum+1, numbers=numbers)
    varslist.append(vars)
    # Empirical OLH
    vars = empirical_OLH(LocalHashing, d=maxnum+1, numbers=numbers)
    varslist.append(vars)
    
    # Draw
    epss = [0.5+0.5*item for item in range(NUMBEROFAXIS)] # 0.5, 1.0, ..., 5.0
    with open('temp_drawFigure3.py', 'w') as f:
        f.write(str(varslist))
    draw.lines(epss, varslist, ['Empirical BLH', 'Empirical OLH'], title='Figure 3: Average squared error, varying epsilon', xlabel='Vary epsilon(x=epislon)', ylabel='y=log10(Var)')
    

if __name__=='__main__':
    drawFigure3()
