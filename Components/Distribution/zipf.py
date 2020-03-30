
'''
zipf:
param: s, range: n
output : A list with num numbers, ranging from 0 to n-1
'''

def probList(s, n):
    assert n > 0, 'n <= 0'
    if n == 1:
        return num*[0]
    values = []
    sum = 0.0
    for i in range(n):
        temp = 1.0 / ((i+1) ** s)
        values.append(temp)
        sum += temp
    
    f = [] # probabilities
    for i in range(n):
        f.append( values[i] / sum)
    return f

def zipf(s, n, num):
    f = probList(s, n)
    # generate data
    # 0 is the last value to add 
    out = []
    for i in range(n-1):
        out.extend( ( round(num*f[i+1])) * [i+1])
    out.extend( (num-len(out)) * [0])
    return out

if __name__ == "__main__":
    mylist = zipf(1.1, 1024, 10000)
    #print(mylist)
    print(len(mylist))
    