# -*- coding: utf-8 -*-

#%%
"""
This script contains the necessary functions for Performing Inside Outside Test.
Eventually, elements are categorized as Inside, Outside and Cut 
"""
#%%

import numpy as num
from matplotlib import pyplot as plt
import shapely.geometry as shape
from matplotlib import patches
import os

#%%

def Read_Element_List():
    """
    This function reads the element list generated by Abaqus.
    The data structure of this Element_list is as follows:
        Element_list[i]=[Element_Label, nodal_connectivity, flag]
    Input: none
    Output: Element_list
    
    """
    os.chdir("../Data Files")
    foo = open('Element_data_1D_array.txt','r')  # Do not change this file's name
    Element_list = []   # List of lists, each list (temp) contains int, vector,int
    temp = []           #List
    nodal_connectivity = num.zeros(4,int)
    Element_Label=0
    flag = 0    
    num_elem=int(foo.readline())                  #Key : 0 -> Totally outside , 1-> Totaly inside , 2-> Cut element
    for i in range(0,num_elem):
        Element_Label = int(foo.readline())
        for j in range(0,4):
            nodal_connectivity[j] = int(foo.readline())
                
        temp = [Element_Label,nodal_connectivity,flag]
        Element_list.append(temp)
        Element_Label=0
        nodal_connectivity = [0,0,0,0]
    foo.close()
    os.chdir("../Python Scripts")
    return Element_list

#%%

def Read_Nodal_List():
    """
    This function reads the node list generated by Abaqus.
    The data structure of this Node_list is as follows:
        Node_list[i]=[Node_Label,coordinates]
    Input: none
    Output: Element_list
    
    """
    os.chdir("../Data Files")
    fo = open('Node_data_1D_array.txt','r')    # Do not change this file's name
    Node_list = []      # List of lists, each list (temp) contains int and a vector
    temp = []
    coordinates = num.zeros(2)  
    Node_Label = 0
    num_node=int(fo.readline())  
    for i in range(0,num_node):
        Node_Label = int(fo.readline())
        for j in range(0,2):
            coordinates[j] = float(fo.readline())
            if(abs(coordinates[j])<0.000001):
                coordinates[j] =0.0
                
        temp = [Node_Label,coordinates]
        Node_Label=0
        coordinates = [0.0,0.0]
        Node_list.append(temp)   
    fo.close()
    os.chdir("../Python Scripts")
    return Node_list

#%%

def In_or_out(My_geometry,Element_list,Node_list,Phy_domain):
    """
    This function performs the Inside_Outside test for all elements and categorize them into:
        * Inside, flag set to -> 1
        * Cut, flag set to -> 2
        * Outside, flag set to -> 0
    An updated element list is generated with the following data structure:
        Element_list_updated = [outside,inside,intersect], where
        outside: a List containing label of the elements outside
        inside: a List containing label of the elements inside
        intersect: a List containing label of the elements cut
        
    Input: Element_list,Node_list,Phy_domain,left_corner,length,height
    Output: Element_list_updated
    
    """
    
    #Getting co-ordinates of minimum and maximum points to compute the bounding box
    Max_cord = My_geometry.max_
    Min_cord = My_geometry.min_
    
    Xmin = Min_cord[0]
    Ymin=  Min_cord[1]
    Xmax = Max_cord[0]
    Ymax = Max_cord[1]
          
    #Parameters for the Rectangular patch
    left_corner = (Xmin,Ymin)
    length = Xmax - Xmin
    height = Ymax-Ymin
    # Visualizing the bounding box    
    Element_list_updated = []
    fig = plt.figure()
    ax = fig.add_subplot(111,aspect='equal')
    Xmin = left_corner[0]
    Ymin=  left_corner[1]
    Xmax = left_corner[0] + length
    Ymax = left_corner[1] + height
    Box= patches.Rectangle(left_corner,length,height,fill = False ,linestyle = 'dashed',linewidth = 3.0,color = 'black')
    ax.add_patch(Box)
    plt.ylim((Ymin -10),(Ymax+10))
    plt.xlim((Xmin-10),(Xmax+10))
    fig.show()
     
    # Performing the Inside Outside test    
    Domain = shape.Polygon(Phy_domain)
    Num_of_elements = len(Element_list)
    intersect = []
    inside = []
    outside = []
    plt.figure(2)
    plt.title('Inside Outside and Cut Elements ')
    # Loop over all elements    
    for i in range(0,Num_of_elements):
        # Get Nodes Label for an element
        Node_SW = Element_list[i][1][0]
        Node_SE = Element_list[i][1][1]
        Node_NE = Element_list[i][1][2]
        Node_NW = Element_list[i][1][3]
        
        # Get the coordinates of an element's nodes
        cord_Node_SW = Node_list[Node_SW][1]
        cord_Node_SE = Node_list[Node_SE][1]
        cord_Node_NE = Node_list[Node_NE][1]
        cord_Node_NW = Node_list[Node_NW][1]
        
        # Create the polygon
        i_th_Element = shape.Polygon([(cord_Node_SW),(cord_Node_SE),(cord_Node_NE),(cord_Node_NW)])
        x,y = i_th_Element.exterior.xy
        
        # Check the created polygon with the Physical domain
        if Domain.contains(i_th_Element) :               # Check for Inside
        
            Element_list[i][2] = 1
            inside.append(Element_list[i][0])
            x,y = i_th_Element.exterior.xy
            plt.plot(x,y,color='Green', linewidth = 1.0) # Plot Inside Elements
            
        elif i_th_Element.intersects(Domain):            # Check for Cut
        
            Element_list[i][2] = 2
            intersect.append(Element_list[i][0])
            x,y = i_th_Element.exterior.xy
            plt.plot(x,y,color='blue', linewidth = 2.0)  # Plot Intersected Elements
        
        else:                                            # Otherwise it is Outside
            Element_list[i][2] = 0
            outside.append(Element_list[i][0])
            x,y = i_th_Element.exterior.xy
            plt.plot(x,y,color='Red', linewidth = 4.0)   # Plot Outside Elements

    
    Element_list_updated = [outside,inside,intersect]
    

    # Writing the Element_list for abaqus to create element sets    
    os.chdir("../Data Files")
    foo = open('Outside_elements.txt','w')     # Do not change this file's name
    num.savetxt(foo,Element_list_updated[0])
    foo.close()
    
    foo = open('Cut_elements.txt','w')        # Do not change this file's name
    num.savetxt(foo,Element_list_updated[2])
    foo.close()
    
    foo = open('Inside_Elements.txt','w')     # Do not change this file's name
    num.savetxt(foo,Element_list_updated[1])
    foo.close()
    os.chdir("../Python Scripts")
    
    print('Inside Outside Test Successfully Completed \n')
    return Element_list_updated
    