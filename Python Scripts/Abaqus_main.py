# -*- coding: utf-8 -*-

#%%
"""
This script is to be run by Abaqus CAE and it performs the following tasks:
    1- Create part
    2- Generate structured mesh
    3- Create material definitions
    4- Create section definitions
    5- Assign section properties
    6- Create element sets
    7- Create a step for analysis
    8- Apply Boundary Conditions (only valid for a rectangular/square plate as 
       the outer boundary of the physical domain)
    9- Generate Input file
"""
#%%

from load import *
from job import *
import numpy as num
import Abaqus_functions as ABAQUS 
import Utility_functions_ABAQUS as Util
import os

#%%

def main():
  
###############################################################################
    
    #Parameters to be entered
    
    Elastic_modulus = 200000        #(N/mm^2)
    Poisson_Ratio = 0.3
    Thickness = 1.0                 #Thickness of the plane stress element (mm)
    Epsilon = 0.0000000001          # Set this value to define stiffness for outside elements
    
##############################################################################3
    
    
    mesh_filename = 'Mesh_Parameters.txt'    # Do not change this file's name
    mesh_size = 0.0
    Rectangle = num.zeros((2,2))
    sheet_size = 0.0
    
    os.chdir("../Data Files")
    f=open(mesh_filename,'r')
    mesh_size = float(f.readline())
    Rectangle = num.zeros((2,2))
    Rectangle[0][0] = float(f.readline())
    Rectangle[0][1] = float(f.readline())
    Rectangle[1][0] = float(f.readline())
    Rectangle[1][1] = float(f.readline())
    sheet_size = float(f.readline())  
    f.close()
    os.chdir("../Python Scripts")
    
##############################################################################
    
    #Part creation
    ABAQUS.Create_Part(sheet_size, Rectangle)
       
###############################################################################
    
    #Mesh generation
    ABAQUS.Generate_Mesh(mesh_size, Rectangle)    
       
##############################################################################
    
    #Computing the number of nodes and elements
    
    element_data  = mdb.models['Model-1'].parts['Part-1'].elements
    node_data  = mdb.models['Model-1'].parts['Part-1'].nodes
    
    Num_of_Elem = len(element_data)
    Num_of_Nodes = len (node_data)
    
###############################################################################
    
    #Writing the element and node data to the text files    
    
    file_name_elem = 'Element_data_1D_array.txt'     # Do not change this file's name
    file_name_node = 'Node_data_1D_array.txt'        # Do not change this file's name
    Util.Write_Ele_Node_Data_To_File (file_name_elem, file_name_node, Num_of_Elem, Num_of_Nodes, element_data, node_data )
    
###############################################################################
    
    #Generate orphan mesh
    
    #Creating an alias for the Abaqus part object
    p = mdb.models['Model-1'].parts['Part-1']
    #Creating an alias for the Abaqus model object
    M = mdb.models['Model-1']
    #Creating an alias for the Abaqus ophan part object
    P = ABAQUS.Generate_Orphan_Mesh (p)
     
    #deleting the orginal part an retaining only the orphan mesh object
    del mdb.models['Model-1'].parts['Part-1']
    
##############################################################################
    
    # Create a list of cut elements
    file_name = 'Cut_elements.txt'      # Do not change this file's name
    os.chdir("../Python Scripts")
    element_list_cut = Util.Get_Element_list(file_name)
        
    # Create a list of outside elements
    file_name = 'Outside_elements.txt'  # Do not change this file's name
    element_list_outside = Util.Get_Element_list(file_name)
    
    # Create a list of inside elements
    file_name = 'Inside_Elements.txt'   # Do not change this file's name
    element_list_inside = Util.Get_Element_list(file_name)
    
###############################################################################
   
    ##Create_element sets 
    
    #Creating an alias for the Abaqus element array oject
    e = P.elements
    
    #Creating element set for cut elements
    Set_name = 'Cut'
    ABAQUS.Create_Element_Sets (e,element_list_cut,P,Set_name)
    
    #Creating element set for inside elements   
    Set_name = 'Inside'
    ABAQUS.Create_Element_Sets (e,element_list_inside,P,Set_name)
    
    #Creating element set for inside elements   
    Set_name = 'Outside'
    ABAQUS.Create_Element_Sets (e,element_list_outside,P,Set_name)
    
###############################################################################
    
    ### Create Material   
    ABAQUS.Create_Material (M, Elastic_modulus, Epsilon, Poisson_Ratio)
        
###############################################################################
    
    # Creating sections
    ABAQUS.Create_Solid_Section (M,Thickness)
    
###############################################################################
    
    #Assigning sections    
    ABAQUS.Assign_Sections (P,M)   
    
###############################################################################
    
    #Creating assembly  
    M.rootAssembly.Instance(name = 'Orphan_Mesh_Assembly', part = P)
    
###############################################################################
    
    #Creating Step  
    M.StaticStep(name = 'Static_load_case', previous = M.steps['Initial'].name)
    
###############################################################################
#%%
    """
    The following section of code is only valid for a rectangular/square plate as 
    the outer boundary of the physical domain

    The loading conditons, Nodes for applying conditons for other problems are different
    Comment the following section and use the GUI to apply load and BCs
    """
   
    #Creating Node sets for Dirichlet and Nuemann BC
    ABAQUS.Create_Node_Sets_For_Load_BC (P,M,Rectangle)
    
###############################################################################
    
    #Creating Dirichlet BC
    
    #Fixing y displacement for all the nodes on the bottom edge
    M.DisplacementBC(name='Y_disp_fixed', createStepName = M.steps['Static_load_case'].name, region=M.rootAssembly.sets['BC_X_dirichlet'], u2=0.0)
    
    #Fixing x displacement for all the nodes on the left edge
    M.DisplacementBC(name='X_disp_fixed', createStepName = M.steps['Static_load_case'].name, region=M.rootAssembly.sets['BC_Y_dirichlet'], u1=0.0)
    
###############################################################################
    
    #Creating Dirichlet BC
    #Surface traction applied on the top surface
    M.SurfaceTraction(name = 'Surface_traction', createStepName = M.steps['Static_load_case'].name, region = M.rootAssembly.surfaces['Loading_edge'], magnitude = 100.0, directionVector = ((0.0,0.0,0.0),(0.0,1.0,0.0),), traction = GENERAL) 
    
###############################################################################
    
    #Creating Job   
    Job = mdb.Job(name='Test_run', model = M)
    #Creating the input file
    os.chdir("../Input File and UEL")
    Job.writeInput()
    foo=open('Counter.txt', 'w')       # Do not change this file's name
    foo.write('0')
    foo.close()
    os.chdir("../Python Scripts")
    
###############################################################################
#%%

main()

#%%