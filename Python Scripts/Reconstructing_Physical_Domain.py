# -*- coding: utf-8 -*-

#%%
"""
This script contains the necessary functions for the reconstruction of the Physical domain from
traingles data got from the stl file to a Polygon object, where shapely library attributes can be
used in later stages 
"""
#%%

from matplotlib import patches
from matplotlib import pyplot as plt
import shapely.geometry as shape
import os

#%%

def Compute_Bounding_Box(My_geometry):
    """
    This function creates FCM extended domain "Bounding Box" and plots it into consule
    
    Input: My_geometry
    Output: None
    
    """
    # Coordinates of minimum and maximum points to compute the bounding box
    Max_cord = My_geometry.max_
    Min_cord = My_geometry.min_
    Xmin = Min_cord[0]
    Ymin=  Min_cord[1]
    Xmax = Max_cord[0]
    Ymax = Max_cord[1]
          
    # Parameters for the Rectangular patch
    left_corner = (Xmin,Ymin)
    length = Xmax - Xmin
    height = Ymax-Ymin
       
    # Creating the Bounding box
    Bounding_box = patches.Rectangle(left_corner,length,height,fill = False,linestyle = 'dashed',linewidth = 2.0,color = 'r')
    
    # Plotting the Bounding Box
    fig=plt.figure(1)
    plt.gca().set_aspect("equal")
    plt.axis('off')
    ax=fig.add_subplot(111,aspect="equal")
    ax.add_patch(Bounding_box)
    plt.ylim((Ymin -10),(Ymax+10))
    plt.xlim((Xmin-10),(Xmax+10))
    
#%%

def Visualize_stl_Geometry(No_Triangles,Triangle_data):
    """
    This function plots stl file triangles to one plot in order to visualize the physical domain
    
    Input: fig,ax1,No_Triangles,Triangle_data
    Output: None
    
    """
    
    fig=plt.figure(1)
    ax=fig.add_subplot(111,aspect="equal")
    plt.title (' Physical Geometry from stl file ')
    # Loop over all triangles
    for i in range (0,No_Triangles):
        V1 = Triangle_data[i][0]    # Triangle's 1st vertex
        V2 = Triangle_data[i][1]    # Triangle's 2nd vertex
        V3 = Triangle_data[i][2]    # Triangle's 3rd vertex
        V1_xy = [V1[0],V1[1]]
        V2_xy = [V2[0],V2[1]]
        V3_xy = [V3[0],V3[1]]
        points = [V1_xy,V2_xy,V3_xy]  
        i_th_triangle = patches.Polygon(points)
        ax.add_patch(i_th_triangle)    # Plot triangle

#%%#
        
def write_structured_mesh_param (mesh_filename,My_geometry,No_Triangles,number_of_divisions):
    """
    This function writes a .txt file containing structured mesh parameters to be read by Abaqus for mesh generation
    
    Input: mesh_filename,mesh_size,Xmin,Ymin,Xmax,Ymax,sheet_size,No_Triangles
    Output: None
    
    """
    
    # coordinates of minimum and maximum points of FCM extended domain
    Max_cord = My_geometry.max_
    Min_cord = My_geometry.min_
    Xmin = Min_cord[0]
    Ymin=  Min_cord[1]
    Xmax = Max_cord[0]
    Ymax = Max_cord[1]
          
    #Parameters 
    length = Xmax - Xmin
    height = Ymax-Ymin
    mesh_size = min(length,height) / number_of_divisions
    sheet_size = max(length,height)*1.5 

    # Start writing to txt file
    os.chdir("../Data Files")
    fo = open(mesh_filename,'w')
    fo.write(str(mesh_size)+'\n')
    fo.write(str(Xmin)+'\n')
    fo.write(str(Ymin)+'\n')
    fo.write(str(Xmax)+'\n')
    fo.write(str(Ymax)+'\n')
    fo.write(str(sheet_size) + '\n')
    fo.write(str(No_Triangles)+'\n')
    fo.close()
    os.chdir("../Python Scripts")
    
#%%
    
def Compute_physical_domain(Triangle_List):
    """
    This function creates the physical domain as one polygon by taking
    the union of triangles obtained from .stl file
    
    Input: List of triangles
    Output: Physical domain as a Polygon
    
    """

    num_triangle =  len(Triangle_List)
    
    t=[]    # a temporary list of triangular Polygons
    Physical_geometry = shape.Polygon() # Declaring an object of type Polygon
    
    for  i in range (0,num_triangle):

        V1_xy = [Triangle_List[i][0][0],Triangle_List[i][0][1]]
        V2_xy = [Triangle_List[i][1][0],Triangle_List[i][1][1]]
        V3_xy = [Triangle_List[i][2][0],Triangle_List[i][2][1]]
        
        Point_list = [V1_xy,V2_xy,V3_xy]    # List of all vertices of a triangle     
       
        i_th_triangle = shape.Polygon(Point_list)   # Creating a triangular Polygon
        t.append(i_th_triangle)
        
    
    # Union of all triangular Polygons
    for i in range(0, num_triangle):
        Physical_geometry = Physical_geometry.union(t[i])

    print('Physical Domain Successfully Reconstructed \n')
    return Physical_geometry

#%%
