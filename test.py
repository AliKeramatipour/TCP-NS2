# function to get unique values 
def unique(list1): 
      
    # insert the list to the set 
    list_set = set(list1) 
    # convert the set to the list 
    unique_list = (list(list_set)) 
    unique_list.sort()
    for x in unique_list: 
        print x, 
      
  
# driver code 
list1 = [10, 20, 10, 30, 40, 40] 
print("the unique values from 1st list is") 
unique(list1) 