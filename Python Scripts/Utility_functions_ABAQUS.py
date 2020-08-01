# -*- coding: utf-8 -*-

"""
This file contains all the utility functions needed to exceute the code in ABAQUS
"""
#%%

import numpy as num
import os

#%%

def Write_Ele_Node_Data_To_File (file_name_elem, file_name_node, Num_of_Elem, Num_of_Nodes, element_data, node_data):
    """
    This function writes the element and node data to spearate text files in the required format 

    Format for Element data      : Element label
                               SW node number
                               SE node number
                               NE node number
                               NW node number
                               
                               Format for Node data         : Node number
                               x - coordinate
                               y - coordinate
                               
                               
    Input : file_name_elem, file_name_node, Num_of_Elem, Num_of_Nodes, element_data, node_data
    Ouput : None 
    """
    
    #Writing element data to file in the required format  
    os.chdir("../Data Files")
    Myfile1 = open(file_name_elem,'w')
    Myfile1.write(str(Num_of_Elem)+'\n')
    
    for i in range (0,Num_of_Elem,1):
        
        SW = int(element_data[i].connectivity[0])
        SE = int(element_data[i].connectivity[1])
        NE = int(element_data[i].connectivity[2])
        NW = int(element_data[i].connectivity[3])
        
        elem = int(element_data[i].label)
        
        Myfile1.write(str(elem)+ '\n')
        Myfile1.write(str(SW)+'\n')
        Myfile1.write(str(SE)+'\n')
        Myfile1.write(str(NE)+'\n')
        Myfile1.write(str(NW)+'\n')
        
    Myfile1.close()
    
    ###########################################################################
    
    #Writing node data to file in the required format
    
    Myfile2=open(file_name_node,'w')
    Myfile2.write(str(Num_of_Nodes)+'\n')
    
    for i in range (0,Num_of_Nodes,1):
        
        x = float(node_data[i].coordinates[0])
        y = float(node_data[i].coordinates[1])
        
        node = int(node_data[i].label)
        
        Myfile2.write(str(node)+ '\n')
        Myfile2.write(str(x)+ '\n')
        Myfile2.write(str(y)+ '\n')
    
    Myfile2.close()
    os.chdir("../Python Scripts")

#%%
    
def create_element_list(filename,Num_of_Elem):
    """
    This function creates a list of elements from a given text list
    
    The data structure of the element list is as follows :
        
        Element_list[i] = [index, nodal_connectivity, flag]
        where:
            index -> the label for the element
            nodal -> nodal connectivity in counter clockwise direction starting with the South_West node
            flag  -> key to identify if element is cut, inside or outside
    
    
    Input : Filename to be read from, Number of elements
    Output : List of all Elements
    """
    os.chdir("../Data Files")
    foo = open('Element_data_1D_array.txt','r')
    Element_list = []
    temp = []
    nodal_connectivity = num.zeros(4,int)
    index=0
    flag = 0                               #Key : 0 -> Totally inside, 1-> Totaly outside, 2-> Cut element
    
    #looping over all the elements
    for i in range(1,Num_of_Elem):
        index = int(foo.readline())
        for j in range(0,4):
            nodal_connectivity[j] = int(foo.readline())
            
        temp = [index,nodal_connectivity,flag]
        Element_list.append(temp)
        index=0                           # Re-initialising the variable for next loop  
        nodal_connectivity = [0,0,0,0]    # Re-initialising the variable for next loop
   
    foo.close()
    os.chdir("../Python Scripts")
    
    return Element_list

#%%
    
def create_node_list(filename,NumNodes):
    """
    This function creates a list of nodes from a given text list
    
    The data structure of the node list is as follows :
        
        Node_list[i] = [index, [corodinates]]
        where:
            index -> the label for the node
            [coordinates] ->  list of x and y coordinates [x,y]
    
    Input : Filename to be read from, Number of nodes
    Output : List of all Nodes
    """
    os.chdir("../Data Files")
    fo = open(filename,'r')
    Node_list = []
    temp = []
    coordinates = num.zeros(2)
    index = 0
    index = int(fo.readline())
    
    #looping over all the nodes
    for i in range(1,NumNodes):        
        for j in range(0,2):
            coordinates[j] = float(fo.readline())
            if(abs(coordinates[j])<0.000001):
                coordinates[j] =0.0
            
        temp = [index,coordinates]
        index=0                         # Re-initialising the variable for next loop 
        coordinates = [0.0,0.0]         # Re-initialising the variable for next loop 
        Node_list.append(temp)
        
    fo.close()
    os.chdir("../Python Scripts")
    
    return Node_list
#%%
    
def Get_Element_list (file_name) :
    """
    This functions returns a list of element labels of cut/inside/outside

    Input : Text file name containing the element labels:
    Output : List of element labels
    """
    os.chdir("../Data Files")
    foo = open(file_name,'r')
    element_list = num.loadtxt(foo)
    foo.close
    os.chdir("../Python Scripts")
    
    return element_list

#%%