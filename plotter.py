import nstrace
import sys
import matplotlib.pyplot as plt

RUNNUM = 10
TIMELIMIT = 1000
list1 = []
list2 = []
ll1 = []
ll2 = []
timeVals = []
ptr = []

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
    tmp = 0
    for i in range(ptr[id],len(ll1[id])):
        if ll1[id][i] <= time:
            res = ll2[id][i]
            tmp = i
    ptr[id] = tmp
    return res

def plotAtt(protocolname, varName, srcNode, clr, lbl):
    global ll1, ll2, timeVals,ptr
    ll1 = []
    ll2 = []
    plotter(protocolname, varName, srcNode)
    for i in range(0,RUNNUM):
        ptr[i] = 0
    
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
    plotAtt("Newreno", varName, 0, "red",  "NewReno, c1")
    plotAtt("Newreno", varName, 1, "blue", "NewReno, c2")

    plotAtt("Tahoe", varName, 0, "purple", "Tahoe, c1")
    plotAtt("Tahoe", varName, 1, "yellow", "Tahoe, c2")

    plotAtt("Vegas", varName, 0, "orange", "Vegas, c1")
    plotAtt("Vegas", varName, 1, "green", "Vegas, c2")

    plt.legend(loc='best')
    plt.show()

for i in range(0, RUNNUM):
    ptr.append(0)

plotALL("rtt_")








