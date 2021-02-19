import math
import matplotlib.pyplot as plt
import numpy as np
import sys
import re

def mainProgram(length=250, min_val = -20, max_val = 20, amp=200, plot=False):
    current = [0]*length
    counts = [0]*length

    np.random.seed(1729)
    counts_noise = 0.05 * amp * np.random.normal(size=length)

    for i in range(length):
        current[i] = min_val+(i/length*(max_val-min_val))
        counts[i] = amp*math.sin(2*math.pi*(i/length+i/(2*length)))+amp + counts_noise[i]

    if plot == True:
        plt.clf()
        plt.close()
        plt.plot(current, counts , '-o')
        plt.title('Test Counts')
        plt.xlabel('Current (A)')
        plt.ylabel('Counts (n)')
        plt.show()

    f = open("TestFiles/TestCounts" + str(length) + "_" + str(min_val) + "_" + str(max_val) + "_" + str(amp) + ".txt","w+")
    f.write("Current(A)\tCounts(n)\n")
    for i in range(length):
        f.write("{:8.4f}\t{:8.4f}\n".format(current[i], counts[i]))
    f.close()

if __name__ == '__main__':	
    if len(sys.argv)>1:
        if len(sys.argv)==6:
            mainProgram(length = int(sys.argv[1]), min_val = int(sys.argv[2]), max_val = int(sys.argv[3]),  amp = int(sys.argv[4]), plot=True)
        elif len(sys.argv)==5:
            mainProgram(length = int(sys.argv[1]), min_val = int(sys.argv[2]), max_val = int(sys.argv[3]),  plot=True)
        elif len(sys.argv)==3:
            mainProgram(length = int(sys.argv[1]), plot=True)
        else:
            mainProgram(length = int(sys.argv[1]))
    else:
        print("Usage: python TestCounts.py length min max amp plot=True")
        mainProgram()