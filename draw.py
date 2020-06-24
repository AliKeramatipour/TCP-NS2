from matplotlib import pyplot as plt
list2 = []
list1 = []
file1 = open("tcp0_Tahoe_CWND","r+")  
file2 = open("tcp1_Tahoe_CWND","r+")  
for i in file1:
 list1.append(i.split(", ")[0])
 list2.append(i.split(", ")[1][:len(i.split(", ")[1])-1])
 
plt.plot(list1,list2) 
list2 = []
list1 = []
for i in file2:
 list1.append(i.split(", ")[0])
 list2.append(i.split(", ")[1][:len(i.split(", ")[1])-1])
plt.plot(list1,list2, color="red") 
plt.show()