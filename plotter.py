import nstrace
import sys
import matplotlib.pyplot as plt
import math

RUNNUM = 10
TIMELIMIT = 1000
ll1 = []
ll2 = []
timeVals = []
ptr = []

def plotter(protocolname, varName, srcNode):
    total = 0.0
    dropped = 0.0
    for i in range(0,RUNNUM):
        list1 = []
        list2 = []
        nstrace.nsopen(protocolname +"/" + protocolname + str(i) + ".tr")
        while not nstrace.isEOF():
            if nstrace.isVar():
                (time, src_node, dummy, dummy, dummy, name, val) = nstrace.getVar()
                if time > TIMELIMIT:
                    break;
                if name == varName and src_node == srcNode:
                    list1.append(time)
                    list2.append(val * (100 if varName == "rtt_" else 1))
            elif varName == "loss":
                (event, time, dummy, dummy, dummy, dummy, dummy, dummy, src_node, dummy, dummy, dummy) = nstrace.getEvent()
                if time > TIMELIMIT:
                    break;
                if src_node[0] == srcNode and event == 'd':
                    dropped +=1
                    list1.append(time)
                    list2.append(1)
            else:
                nstrace.skipline()
        ll1.append(list1)
        ll2.append(list2)

def getFunc(id, time):
    res = 0
    tmp = 0
    for i in range(ptr[id],len(ll1[id])):
        if ll1[id][i] <= time:
            res = ll2[id][i]
            tmp = i
    ptr[id] = tmp
    return res

def getDensity(id, time):
    tmp = 0
    cnt = 0
    for i in range(ptr[id],len(ll1[id])):
        if time - 1 < ll1[id][i] and ll1[id][i] <= time:
            cnt += 1
            tmp = i
    ptr[id] = tmp
    return cnt

def plotAtt(protocolname, varName, srcNode, clr, lbl):
    global ll1, ll2, timeVals, ptr
    ll1 = []
    ll2 = []
    plotter(protocolname, varName, srcNode)
    for i in range(0,RUNNUM):
        ptr[i] = 0
    
    finalVals = []
    for time in timeVals:
        avgVal = 0.0
        for i in range(0,RUNNUM):
            if varName == 'ack_' or varName == 'loss':
                avgVal += getDensity(i,time)
            else:
                avgVal += getFunc(i,time)

        avgVal = avgVal / RUNNUM
        finalVals.append(avgVal)
    plt.plot(timeVals, finalVals, color = clr, label = lbl) 

timeVals = range(0,TIMELIMIT+1)
def plotALL(varName,title):
    plt.title(title)
    plotAtt("Newreno", varName, 0, "red",  "Newreno, c1")
    plotAtt("Newreno", varName, 1, "blue", "Newreno, c2")

    plotAtt("TCP", varName, 0, "purple", "Tahoe, c1")
    plotAtt("TCP", varName, 1, "yellow", "Tahoe, c2")

    plotAtt("Vegas", varName, 0, "orange", "Vegas, c1")
    plotAtt("Vegas", varName, 1, "green", "Vegas, c2")

    plt.legend(loc='best')
    plt.xlabel('time')
    plt.ylabel('value')

    if varName != 'loss':
        axes = plt.gca()
        axes.set_ylim([-0.1,None])
        axes.set_xlim([-0.1,None])

    plt.show()

for i in range(0, RUNNUM):
    ptr.append(0)

plotALL("loss", "GOODPUT")








