import math
import matplotlib.pyplot as plt
import sys
import re

def mainProgram(length=250, plot=False):
    min_val = -20
    max_val = 20
    current = [0]*length
    counts = [0]*length

    for i in range(length):
        current[i] = -20+(i/length*(max_val-min_val))
        counts[i] = 200*math.sin(2*math.pi*(i/length+i/(2*length)))+200

    if plot == True:
        plt.clf()
        plt.close()
        plt.plot(current, counts , '-o')
        plt.title('Test Counts')
        plt.xlabel('Current (A)')
        plt.ylabel('Counts (n)')
        plt.show()

    f = open("TestCounts.txt","w+")
    f.write("Current(A)\tCounts(n)\n")
    for i in range(length):
        f.write("{:8.4f}\t{:8.4f}\n".format(current[i], counts[i]))
    f.close()

if __name__ == '__main__':	
    if len(sys.argv)>1:
        if len(sys.argv)==3:
            mainProgram(length = int(sys.argv[1]), plot=True)
        else:
            mainProgram(length = int(sys.argv[1]))
    else:
        mainProgram()