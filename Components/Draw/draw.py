import matplotlib.pyplot as plt
def line(X, Y, label=[], title='Numerical values of Var[c(i)]', xlabel='Vary epislon', ylabel='Var'):
    plt.scatter(X, Y) # draw points
    plt.plot(X, Y, label=label) # draw the line
    plt.legend(loc='best') #
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def lines(X, Ys, labels=[], title='Numerical values of Var[c(i)]', xlabel='Vary epislon', ylabel='Var'):
    #draw points
    for i in range(len(Ys)):
        plt.scatter(X, Ys[i])
    #draw lines
    for i in range(len(Ys)):
        plt.plot(X, Ys[i], label=labels[i])
    plt.legend(loc='best') #
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()