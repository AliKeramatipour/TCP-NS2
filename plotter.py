import nstrace
import sys
import matplotlib.pyplot as plt

RUNNUM = 2
TIMELIMIT = 1000
list1 = []
list2 = []
ll1 = []
ll2 = []
timeVals = []


def plotter(protocolname, varName, srcNode):
    total = 0
    dropped = 0
    for i in range(0,RUNNUM):
        nstrace.nsopen(protocolname +"/" + str(i) + ".tr")
        while not nstrace.isEOF():
            if nstrace.isVar():
                (time, src_node, dummy, dummy, dummy, name, val) = nstrace.getVar()
                if time > TIMELIMIT:
                    break;
                if name == varName: 
                    if src_node == srcNode:
                        list1.append(time)
                        list2.append(val)
            elif varName == "d":
                (event, time, dummy, dummy, dummy, dummy, dummy, dummy, src_node, dummy, dummy, dummy) = nstrace.getEvent()
                if time > TIMELIMIT:
                    break;
                if src_node[0] == srcNode:
                    if event == '-':
                        total+=1
                        list1.append(time)
                        list2.append((dropped*100.0)/total)
                    elif event == 'd':
                        dropped +=1
                        list1.append(time)
                        list2.append((dropped*100)/total)
            else:
                nstrace.skipline()

        ll1.append(list1)
        ll2.append(list2)

def getFunc(id, time):
    res = 0
    for i in range(0,len(ll1[id])):
        if ll1[id][i] < time:
            res = ll2[id][i]
    return res

def plotAtt(protocolname, varName, srcNode, clr, lbl):
    global ll1, ll2, timeVals
    ll1 = []
    ll2 = []
    plotter(protocolname, varName, srcNode)
    finalVals = []
    for time in timeVals:
        avgVal = 0
        for i in range(0,RUNNUM):
            avgVal += getFunc(i,time)
        avgVal = avgVal / RUNNUM
        finalVals.append(avgVal)
    if varName == "ack_":
        for i in range(1,len(timeVals)):
            finalVals[i] = finalVals[i] * 8/i
    plt.plot(timeVals, finalVals, color = clr, label = lbl) 

timeVals = range(0,TIMELIMIT+1)
def plotALL(varName):
    plotAtt("Reno", varName, 0, "red",  "Reno, c1")
    plotAtt("Reno", varName, 1, "blue", "Reno, c2")

    plotAtt("Tahoe", varName, 0, "purple", "Tahoe, c1")
    plotAtt("Tahoe", varName, 1, "yellow", "Tahoe, c2")

    plotAtt("Vegas", varName, 0, "orange", "Vegas, c1")
    plotAtt("Vegas", varName, 1, "green", "Vegas, c2")

    plt.legend(loc='best')
    plt.show()

plotALL("rtt_")








