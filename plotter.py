import nstrace
import sys
import matplotlib.pyplot as plt

list1 = []
list2 = []

def plotter(protocolname, varName, srcNode):
    nstrace.nsopen(protocolname + ".tr")
    while not nstrace.isEOF():
        if nstrace.isVar():
            (time, src_node, src_port, dest_node, dest_port, name, val) = nstrace.getVar()
            if name == varName: 
                if src_node == srcNode:
                    list1.append(time)
                    list2.append(val)
        else:
            nstrace.skipline()

def plotAtt(protocolname, varName, srcNode, clr, lbl):
    global list1,list2
    list1 = [] 
    list2 = []
    plotter(protocolname, varName, srcNode)
    plt.plot(list1,list2, color = clr, label = lbl) 

plotAtt("Reno", "cwnd_", 0, "red",  "Reno, c1")
plotAtt("Reno", "cwnd_", 1, "blue", "Reno, c2")

plotAtt("Tahoe", "cwnd_", 0, "purple", "Tahoe, c1")
plotAtt("Tahoe", "cwnd_", 1, "yellow", "Tahoe, c2")

plotAtt("Vegas", "cwnd_", 0, "orange", "Vegas, c1")
plotAtt("Vegas", "cwnd_", 1, "green", "Vegas, c2")

plt.legend(loc='best')
plt.show()