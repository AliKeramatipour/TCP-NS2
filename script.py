import os
protArr = ['TCP','TCP/Vegas','TCP/Newreno']
for prot in protArr:
    for i in range(10):
        os.system('ns basic1.tcl ' + prot + ' ' + str(i))
