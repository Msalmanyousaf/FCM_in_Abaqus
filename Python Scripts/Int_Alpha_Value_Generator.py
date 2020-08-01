# -*- coding: utf-8 -*-

#%%

from shapely.geometry import Point
from matplotlib import pyplot as plt
#%%

def Integ_Alpha_Value_Generator(Phy_domain,Leaves_coordinate_list,Alpha_List):
    """
    This function performs inside outside test for each integration point of a cut element and
    generates its alpha factor value (0 or 1) required for adaptive integration.
    An Alpha_List is generated for this purpose. 
    e.g a cut element having 4 leaves with lower left, lower right, upper right and upper left "outside" integration points:
        Alpha_List= [[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]]
    
    Input: Physical domain, Leaves_coordinate_list, empty Alpha_List
    Output: None
    
    """
    
    Leaves_Per_Cell=len(Leaves_coordinate_list)
    
    # Loop over all Leaves of cut element
    for i in range (0,Leaves_Per_Cell):
        temp=[]
        
        # Loop over 4 Integration points per leaf
        for k in range (0,4):
            x=Leaves_coordinate_list[i][2][k]   # Integration Point x coordinate
            y=Leaves_coordinate_list[i][3][k]   # Integration Point y coordinate
            GP=Point(x,y)       # Create a Point object

            # Integration Point Inside Outside test
            if Phy_domain.contains(GP) :  #Check for Integration point Inside and give alpha=1
                temp.append(1)
                plt.plot([x],[y], 'go')     # Plot inside Integration point on physical space
                
            else:  #Otherwise the GP has to be outiside and alpha=0
                temp.append(0)
                plt.plot([x],[y], 'ro')     # Plot outside Integration point on physical space
                
                
        Alpha_List.append(temp)