import nstrace
import sys
import matplotlib.pyplot as plt

RUNNUM = 1

list1 = []
list2 = []
ll1 = []
ll2 = []
timeVals = []


def plotter(protocolname, varName, srcNode):
    for i in range(0,RUNNUM):
        nstrace.nsopen(protocolname + str(i) + ".tr")
        while not nstrace.isEOF():
            if nstrace.isVar():
                (time, src_node, src_port, dest_node, dest_port, name, val) = nstrace.getVar()
                timeVals.append(time)
                if name == varName: 
                    if src_node == srcNode:
                        list1.append(time)
                        list2.append(val)
            else:
                nstrace.skipline()
        list1.append(1001)
        list2.append(list2[-1])
        ll1.append(list1)
        ll2.append(list2)


def plotAtt(protocolname, varName, srcNode, clr, lbl):
    global ll1, ll2, timeVals

    plotter(protocolname, varName, srcNode)
    finalVals = []
    ptr = []
    for i in range(0,RUNNUM):
        ptr.append(0)
    for time in timeVals:
        for i in range(0,RUNNUM):
            while ll1[i][ptr[i]] <= time:
                ptr[i] += 1
            ptr[i] -= 1
        avgVal = 0
        for i in range(0,RUNNUM):
            avgVal += ll2[i][ptr[i]]
        avgVal = avgVal / RUNNUM
        finalVals.append(avgVal)

    print(len(timeVals))
    print(len(finalVals))   
    plt.plot(timeVals, finalVals, color = clr, label = lbl) 

plotAtt("Reno", "cwnd_", 0, "red",  "Reno, c1")
#plotAtt("Reno", "cwnd_", 1, "blue", "Reno, c2")

#plotAtt("Tahoe", "cwnd_", 0, "purple", "Tahoe, c1")
#plotAtt("Tahoe", "cwnd_", 1, "yellow", "Tahoe, c2")

#plotAtt("Vegas", "cwnd_", 0, "orange", "Vegas, c1")
#plotAtt("Vegas", "cwnd_", 1, "green", "Vegas, c2")

plt.legend(loc='best')
plt.show()