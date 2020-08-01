# -*- coding: utf-8 -*-
"""
This file contains all the functions used for ABAQUS

"""
#%%
from sys import path
path.append('C:\Users\salman\Anaconda3\envs\py27\Lib\site-packages')
    
from abaqus import *
import numpy as num
from part import *
from material import *
from section import *
from assembly import *
from step import *
from mesh import *
from sketch import *

#%%

def Create_Part (sheet_size, Rectangle):
    """
    This fucntion creates a part object in ABAQUS.
    
    Input :  Sheet size -> To define the extend of the bounding box
             Rectangle -> Coordinates of extreme points for the structured mesh
             
    Ouput : Abaqus part object
    
    """
    
    #Creating constrained sketch using the sheet size computed earlier
    mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=sheet_size)
    
    #Creating the bounding box for the physical domain
    mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(Rectangle[0][0], Rectangle[0][1]),point2=(Rectangle[1][0], Rectangle[1][1]))
    
    #Creating 2D planar deformable part
    mdb.models['Model-1'].Part(dimensionality=TWO_D_PLANAR, name='Part-1', type=DEFORMABLE_BODY)
    
    #Selecting the sketch neede to create the part
    mdb.models['Model-1'].parts['Part-1'].BaseShell(sketch=mdb.models['Model-1'].sketches['__profile__'])
    
    #delete sketch
    del mdb.models['Model-1'].sketches['__profile__']
    
#%% 
    
def Generate_Mesh(mesh_size, Rectangle):
    
    """
    This fucntion creates a structured mesh in ABAQUS.
    
    Input :  mesh size -> Defines the size of the elements
             Rectangle -> Coordinates of extreme points for the structured mesh
             
    Ouput : Structured mesh
    
    """
    
    #Mapping the regions where the strcutured mesh has to be generated
    mdb.models['Model-1'].parts['Part-1'].setMeshControls(elemShape=QUAD, regions=mdb.models['Model-1'].parts['Part-1'].faces.findAt((((Rectangle[0][0]+mesh_size),(Rectangle[0][1]+mesh_size),0.0), )), technique=STRUCTURED)
    
    #Settung the element type for the mesh
    mdb.models['Model-1'].parts['Part-1'].setElementType(elemTypes=(ElemType(elemCode=CPS4, elemLibrary=STANDARD), ElemType(elemCode=CPS4,
    elemLibrary=STANDARD)), regions=(mdb.models['Model-1'].parts['Part-1'].faces.findAt((((Rectangle[0][0]+mesh_size),(Rectangle[0][1]+mesh_size),0.0), )), ))
    
    #Seeding the mesh (Defining the size of the elements for the structured mesh)
    mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1, size=mesh_size)
    
    #Generate mesh
    mdb.models['Model-1'].parts['Part-1'].generateMesh()

#%%
    
def Generate_Orphan_Mesh (Part_object):
    
    """
    This fucntion creates an orphan mesh from a given structured mesh associated with a part
    
    Input :  Part obect -> Abaqus part  object with structured mesh
                           from which an orphan mesh has to be generated
                        
    Ouput : New part oject (orphan_mesh_part obejct)
    
    """
    
    mdb.meshEditOptions.setValues(enableUndo=True, maxUndoCacheElements=0.5)
    Part_object.PartFromMesh(name='Orphan_mesh', copySets=True)
    
    return mdb.models['Model-1'].parts['Orphan_mesh']

#%% 
    
def Create_Element_Sets (Elem, Element_list, P, Set_name):
    """
    This fucntion creates an element sets
    
    Input :  Elem -> Abaqus Element array object containing details of the elements
             Elements -> A list containing the label of the elements for which sets have to created
             P -> Abaqus part object for which the element sets will be created
             Set_name -> String containg the name of the set to be created
                        
    Ouput : An element set for the oprhan mesh part
    
    """
    elements = []                               # Temporary list to store all the elements in the given set
    Num_of_Elem_per_set = len(Element_list)     # Number of elements in the set
    
    for i in range (0,Num_of_Elem_per_set): 
        im  = int(Element_list[i]-1)        
        ip = int(Element_list[i])
        elements.append(Elem[im:ip])
    
    #Creating the set with  given Set name and elements    
    P.Set(elements=elements, name = Set_name)   
    
#%%
    
def Create_Material (M, Elastic_modulus, Epsilon, Poisson_Ratio):
    """
    This fucntion creates two materials as follows :
        
        Alpha-0 -> Isotropic material with very low stiffness for the elements outside the domain
        Alpha-1 -> Isotropic material with given Stiffness and poisson ration fpr elemets inside the domain
    
    Input :  M               -> Abaqus Model object for which material is being created
             Elastic_modulus -> Stiffness defined by te user for the physical domain
             Poisson_Ration  -> Poisson ratio defined by the user
             Epsilon         -> Factor defined by the user
                        
    Ouput : Two Abaqus material objects
    
    """
    #Cretaing material object for outside elements
    M.Material(name = 'Alpha-0')
    M.materials['Alpha-0'].Elastic(table = ((Elastic_modulus*Epsilon,Poisson_Ratio),),type=ISOTROPIC)
    
    #Cretaing material object for inside elements
    M.Material(name = 'Alpha-1')
    M.materials['Alpha-1'].Elastic(table = ((Elastic_modulus,Poisson_Ratio),),type=ISOTROPIC)
    
#%% 
    
def  Create_Solid_Section (M,Thickness):
    """
    This fucntion creates three homogeous solid section with specifid thickness as follows :
        
        Inside_Elements   ->  Section with material Alpha-1
        Outside_Elements  ->  Section with material Alpha-0
        Cut_Elements      ->  Section with material Alpha-1
        
    Input :  M            -> Abaqus Model object for which sections is being created
             Thickness    -> Thickness of planes stress element defined by the user
             
    Ouput : Three Abaqus Solid section objects
    
    """
    #Section for inside elements
    M.HomogeneousSolidSection(name ='Inside_Elements', material = M.materials['Alpha-1'].name,thickness = Thickness)
    
    #Section for outside elements
    M.HomogeneousSolidSection(name ='Outside_Elements', material = M.materials['Alpha-0'].name,thickness = Thickness)
    
    #Section for cut elements
    M.HomogeneousSolidSection(name ='Cut_Elements', material = M.materials['Alpha-0'].name,thickness = Thickness)
    
#%% 
    
def Assign_Sections (P,M):
    """
    This fucntion assign the created section to the corresponding element sets:
        
    Input :  P            -> Abaqus Part object for which sections are being assigned
                          
    Ouput : None
    
    """
    #Section assignment to inside elements
    P.SectionAssignment(region = P.sets['Inside'],sectionName=M.sections['Inside_Elements'].name)
    
    #Section assignment to outside elements
    P.SectionAssignment(region = P.sets['Outside'],sectionName=M.sections['Outside_Elements'].name)
    
    #Section assignment to cut elements
    P.SectionAssignment(region = P.sets['Cut'],sectionName=M.sections['Cut_Elements'].name)
    
#%%

def Create_Node_Sets_For_Load_BC (P,M,Rectangle): 
    """
    This fucntion creates node sets for application of Dirichlet Boundary condition and Nuemann Boundary condition:
        
    Input :      P   -> Abaqus Part object for which sections are being assigned
                 M   -> Abaqus Model object for which sections are being assigned     
    
    Ouput :     Nodal sets to apply Boundary condition and Loads
    """
    
    Nodes_BC_1_Dirchl = []                              #List of node labels to apply y-displacement constraint
    Nodes_BC_2_Dirchl = []                              #List of node labels to apply x-displacement constraint
    Nodes_BC_3_Nuemm = []                               #List of node labels to apply Tractio force on the top face
    Elem_BC_3_Nuemm=[]                                  #List of Elements to create a surface to apply traction
    
    for i in range(0,len(P.nodes)):
        x = P.nodes[i].coordinates[0]                   # X coordinate of the node
        y = P.nodes[i].coordinates[1]                   # Y coordinate of the node
        
        if y==0.0 and x!=0:                             # Checking if node lies on the bottom edge of plate
            Nodes_BC_1_Dirchl.append(P.nodes[i].label)
    
        if x==0.0 and y!=0:
            Nodes_BC_2_Dirchl.append(P.nodes[i].label)  # Checking if node lies on the top edge of plate
                    
        if x==0.0 and y==0.0:                           # Checking if node lies at the origin
            Nodes_BC_1_Dirchl.append(P.nodes[i].label)
            Nodes_BC_2_Dirchl.append(P.nodes[i].label)
            
        if y==Rectangle[1][1]:                          # Checking if node lies on the top right corner of plate
            Nodes_BC_3_Nuemm.append(P.nodes[i].label)
            
        if y==Rectangle[1][1] and x==0.0:               # Checking if node lies on the bottom right corner of plate
            Nodes_BC_3_Nuemm.append(P.nodes[i].label)
    
    #Creating element sets to create a surface for application of traction
    for i in range (1,len(Nodes_BC_3_Nuemm)-1):
        Elem_BC_3_Nuemm.append(M.rootAssembly.instances['Orphan_Mesh_Assembly'].nodes[Nodes_BC_3_Nuemm[i]].getElements()[0].label)
        
    
      
    #Creating element set to dirichlet condition on the x directions
    M.rootAssembly.SetFromNodeLabels(name='BC_X_dirichlet', nodeLabels = ((M.rootAssembly.instances['Orphan_Mesh_Assembly'].name,(Nodes_BC_1_Dirchl[0:])),))
   
    #Creating element set to dirichlet condition on the y directions
    M.rootAssembly.SetFromNodeLabels(name='BC_Y_dirichlet', nodeLabels = ((M.rootAssembly.instances['Orphan_Mesh_Assembly'].name,(Nodes_BC_2_Dirchl[0:])),))
    
    #Creating element set to Nuemann condition
    M.rootAssembly.SetFromNodeLabels(name='BC_Y_Nuemman', nodeLabels = ((M.rootAssembly.instances['Orphan_Mesh_Assembly'].name,(Nodes_BC_3_Nuemm[0:])),))
    
    #Creating element set to Nuemann condition
    M.rootAssembly.SetFromElementLabels(name='Elem_BC_Y_Nuemman', elementLabels = ((M.rootAssembly.instances['Orphan_Mesh_Assembly'].name,(Elem_BC_3_Nuemm[0:])),))
    
    #Creating surface from the elements
    M.rootAssembly.SurfaceFromElsets(name='Loading_edge', elementSetSeq=((M.rootAssembly.sets['Elem_BC_Y_Nuemman'],S3),))
    
#%%