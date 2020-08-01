# -*- coding: utf-8 -*-

#%%
"""
This script performs QuadTree algorithm to Cut Element and evaluates its Stiffness Matrix
"""
#%%

import numpy as num
from matplotlib import pyplot as plt
from My_CutCell_QuadTree import QuadTree
from Int_Gauss_Point_Generator import Integ_Points_Generator
from Int_Alpha_Value_Generator import Integ_Alpha_Value_Generator
from Map_Integ_points import get_Xi_Eta_Coordinates
from Int_Quad_Cut_Cell import Cut_Element_Integration
import os

#%%

def Perform_QuadTree_And_Generate_K (Updated_Element_list, Element_list, Node_list, Phy_domain):
    """
    This function performs Quad-tree algorithm to cut elements and 
    performs adaptive integration to evaluate their stiffness matrices.
    
    Input : Updated_Element_list, Element_list, Node_list, Phy_domain
    Output: A text file containing the stiffness matrices for the cut elements to be used in ABAQUS UEL
    
    """
    
    print("Cut Cells QuadTree Generation & Stiffness Matrix Calculation Started \n")
    
    Leaves_label_list =[]           # List containing the label of the leaves of a cut element
    Leaves_coordinate_list = []     # List containing (Xmin,Ymin) and (Xmax,Ymax) for each leaf of a cut element
    Alpha_List = []                 # A list specfying if an integration point is inside or outside for each cut element
    Integ_Input_list = []           # A list of Gauss points (Xi, Eta), with weights and alpha values for each cut element
    Xi_Eta_Integ_pts = []           # A list of integration points in the Xi and Eta cordinates for each cut element
    
    maxLevel =3                     # Assign quad tree depth
    E = 200                         # Elastic modulus (N/mm2)
    t = 1                           # Thickness of plane stress element (mm)
    Nu = 0.3                        # Poisson ratio
    
    Num_of_CutCells= len(Updated_Element_list[2]) 
    
    # Loop over the number of cut elements
    for i in range (0,Num_of_CutCells):
        
        del Leaves_coordinate_list[:]
        del Alpha_List[:]
        del Integ_Input_list[:]
    
        CutCellNum =Element_list[Updated_Element_list[2][i]-1][0]       #Label of the cut element
        
        # Node labels of South_West and North_East nodes of the cut element
        Node_SW = Element_list[Updated_Element_list[2][i]-1][1][0]      
        Node_NE = Element_list[Updated_Element_list[2][i]-1][1][2]
             
        Xmin = Node_list[Node_SW][1][0]
        Ymin = Node_list[Node_SW][1][1]
        Xmax = Node_list[Node_NE][1][0]
        Ymax = Node_list[Node_NE][1][1]
               
        tree= QuadTree(CutCellNum,Phy_domain,Xmin, Ymin, Xmax, Ymax, None, 0, "2",0)  # Create an object of type Quadtree
        
        # Generating the Quadtree for the given depth for every cut element
        tree.generateQuadtree(maxLevel)
        plt.figure(3)
        plt.title(" Cut Elements QuadTree ")
        plt.gca().set_aspect("equal")       #To set equal scales for the axes
        tree.plotTreeToConsole()            #Plot Quad-tree for the cut element
        plt.figure(4)
        plt.gca().set_aspect("equal")       #To set equal scales for the axes
        tree.plotTreeToConsole()            #Plot Quad-tree for the cut element
    
        # Generating Input required for Integration:
        # 1- Obtaining the label list for each leaf        
        tree.Return_Label_list(Leaves_label_list)
        
        # 2- Obtaining minimum and maximum bounds for each leaf of a cut element                      
        Leaves_coordinate_list=tree.Return_Leaves_list()
        
        # 3- Generate Integration points for cut elemets with respect to physical space  
        Integ_Points_Generator(Leaves_coordinate_list)

        # 4- Generate alpha value for each integration point of a cut element
        plt.figure(4)
        plt.title(" Cut Elements Integration Points ")
        plt.gca().set_aspect("equal")       #To set equal scales for the axes
        Integ_Alpha_Value_Generator(Phy_domain,Leaves_coordinate_list,Alpha_List) 

        # 5 -Combine Leaves_label_list and Alpha_List 
        for k in range (0,len(Alpha_List)):
            temp = []
            temp.append(Leaves_label_list[k])
            temp.append(Alpha_List[k])
            Integ_Input_list.append(temp)
    
        # 6- Generate integration points with respect to cut element's parametric coordinates
        Xi_Eta_Integ_pts = get_Xi_Eta_Coordinates(Integ_Input_list, CutCellNum) 
        # 7- Corodinates of Cut element's nodes (1-2-3-4)
        Coordinates = [[Xmin,Ymin],[Xmax,Ymin],[Xmax,Ymax],[Xmin,Ymax]] 
          
        # Start Adaptive Integration to Evaluate Cut Element Stiffness Matrix: 
        
        # Create object of type Cut_Element_Integration
        Elem_Integration = Cut_Element_Integration(Coordinates,E,t,Nu,Xi_Eta_Integ_pts) 
        
        # Compute Stiffness matrix for the cut element
        Stiffness_Matrix = Elem_Integration.calculate_elastic_stiffness_matrix()
         
        #Writing the Stiffness matrix to text file to be used for Abaqus UEL
        os.chdir("../Input File and UEL")
        foo = open("Stifness_matrix_Element.txt",'a')  # Do not change this file's name
        num.savetxt(foo,Stiffness_Matrix)
        foo.close()
        os.chdir("../Python Scripts")
        
    print("Cut Cells QuadTree Generation & Stiffness Matrix Calculation Successfully Completed \n")