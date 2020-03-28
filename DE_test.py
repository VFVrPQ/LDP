from DE.DE import DE

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