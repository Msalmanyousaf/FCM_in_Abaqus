# -*- coding: utf-8 -*-

#%%

def Integ_Points_Generator(Leaves_coordinate_list):
    """
    This function generates the integration points for the cut elements with respect to the physical space.
    A mapping of integration points from leaf's parametric space to the physical space is performed.
    2 vectors are added per leaf:
        1- Vector contains the x-coordinates of Integration points mapped from leaf's parametric space
        2- Vector contains the y-coordinates of Integration points mapped from leaf's parametric space
    Integration points convention is as follows:
        1 -> Integration point in the 3rd quadrant
        2 -> Integration point in the 4th quadrant
        3 -> Integration point in the 1st quadrant
        4 -> Integration point in the 2nd quadrant
        
    Input: Leaves_coordinate_list
    Output: None
    
    """
    
    Leaves_Per_Cell=len(Leaves_coordinate_list)     # Number of Leaves per cut element
    
    # Loop over all Leaves of cut element
    for i in range (0,Leaves_Per_Cell):
            
        Xmin= Leaves_coordinate_list[i][0][0]
        Xmax= Leaves_coordinate_list[i][1][0]
        Ymin= Leaves_coordinate_list[i][0][1]
        Ymax= Leaves_coordinate_list[i][1][1]
        deltaX=Xmax-Xmin
        deltaY=Ymax-Ymin
        
        # Map four Integration Points from Leaf's parametric space (Xi-coordinate) to physical space (x-coordinate)
        xCordone=Xmin + (deltaX/2)*(1-0.57735026919)
        xCordtwo=Xmax - (deltaX/2)*(1-0.57735026919)
        xCordthree=xCordtwo
        xCordfour=xCordone
        
        # Map four Integration Points from Leaf's parametric space (Eta-coordinate) to physical space (y-coordinate)
        yCordone=Ymin + (deltaY/2)*(1-0.57735026919)
        yCordtwo=yCordone
        yCordthree=Ymax - (deltaY/2)*(1-0.57735026919)
        yCordfour=yCordthree
        
        # Vectors of x and y coordinates of Integration points per leaf
        xCords=(xCordone,xCordtwo,xCordthree,xCordfour)
        yCords=(yCordone,yCordtwo,yCordthree,yCordfour)
        
        # Add vectors to Leaves_coordinate_list
        Leaves_coordinate_list[i].append(xCords)
        Leaves_coordinate_list[i].append(yCords)
            