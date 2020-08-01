# -*- coding: utf-8 -*-

#%%
"""
This script maps the intergation points of a cut element from its leaves parametric space to
the parametric space of the cut element
"""
#%%

def XiMap1(GpsXiChild):
    """
    This function maps the Xi points present in Quadrant 1 of a leaf
    to its respective father's local coordinates system
    
    Input : GpsXiChild -> List of Xi cordinates of integration points of the child leaf
    Output : GpsXiChild_new - > List of Xi cordinates of integration points mapped to the parent's coordinates
    """
    
    GpsXiChild_new = []
    for i in range (0,4):
        Xi_new = (GpsXiChild[i] - 1)/2.0
        GpsXiChild_new.append(Xi_new)
    
    return GpsXiChild_new

#%%
    
def EtaMap1(GpsEtaChild):
    """
    This function maps the Eta points present in Quadrant 1 of a leaf
    to its respective father's local coordinates system
    
    Input : GpsEtaChild -> List of Eta coordinates of integration points of the child leaf
    Output : GpsEtaChild_new - > List of Eta cordinates of integration points mapped to the parent's coordinates
    """
    
    GpsEtaChild_new = []
    for i in range (0,4):
        Eta_new = (GpsEtaChild[i] - 1)/2.0
        GpsEtaChild_new.append(Eta_new)
    
    return GpsEtaChild_new

#%% 
    
def XiMap2(GpsXiChild):
    """
    This function maps the Xi points present in Quadrant 2 of a leaf
    to its respective father's local coordinates system
    
    Input : GpsXiChild -> List of Xi cordinates of integration points of the child leaf
    Output : GpsXiChild_new - > List of Xi cordinates of integration points mapped to the parent's coordinates
    """
    
    GpsXiChild_new = []
    for i in range (0,4):
        Xi_new = (GpsXiChild[i] + 1)/2.0
        GpsXiChild_new.append(Xi_new)
    
    return GpsXiChild_new

#%%
    
def EtaMap2(GpsEtaChild):
    """
    This function maps the Eta points present in Quadrant 2 of a leaf
    to its respective father's local coordinates system
    
    Input : GpsEtaChild -> List of Eta coordinates of integration points of the child leaf
    Output : GpsEtaChild_new - > List of Eta cordinates of integration points mapped to the parent's coordinates
    """
    
    GpsEtaChild_new = []
    for i in range (0,4):
        Eta_new = (GpsEtaChild[i] - 1)/2.0
        GpsEtaChild_new.append(Eta_new)
    
    return GpsEtaChild_new

#%%
    
def XiMap3(GpsXiChild):
    """
    This function maps the Xi points present in Quadrant 3 of a leaf
    to its respective father's local coordinates system
    
    Input : GpsXiChild -> List of Xi cordinates of integration points of the child leaf
    Output : GpsXiChild_new - > List of Xi cordinates of integration points mapped to the parent's coordinates
    """
    
    GpsXiChild_new = []
    for i in range (0,4):
        Xi_new = (GpsXiChild[i] + 1)/2.0
        GpsXiChild_new.append(Xi_new)
    
    return GpsXiChild_new

#%%
    
def EtaMap3(GpsEtaChild):
    """
    This function maps the Eta points present in Quadrant 3 of a leaf
    to its respective father's local coordinates system
    
    Input : GpsEtaChild -> List of Eta coordinates of integration points of the child leaf
    Output : GpsEtaChild_new - > List of Eta cordinates of integration points mapped to the parent's coordinates
    """
    
    GpsEtaChild_new = []
    for i in range (0,4):
        Eta_new = (GpsEtaChild[i] + 1)/2.0
        GpsEtaChild_new.append(Eta_new)
    
    return GpsEtaChild_new

#%% 
    
def XiMap4(GpsXiChild):
    """
    This function maps the Xi points present in Quadrant 4 of a leaf
    to its respective father's local coordinates system
    
    Input : GpsXiChild -> List of Xi cordinates of integration points of the child leaf
    Output : GpsXiChild_new - > List of Xi cordinates of integration points mapped to the parent's coordinates
    """
    
    GpsXiChild_new = []
    for i in range (0,4):
        Xi_new = (GpsXiChild[i] - 1)/2.0
        GpsXiChild_new.append(Xi_new)
    
    return GpsXiChild_new

#%%
    
def EtaMap4(GpsEtaChild):
    """
    This function maps the Eta points present in Quadrant 4 of a leaf
    to its respective father's local coordinates system
    
    Input : GpsEtaChild -> List of Eta coordinates of integration points of the child leaf
    Output : GpsEtaChild_new - > List of Eta cordinates of integration points mapped to the parent's coordinates
    """
    
    GpsEtaChild_new = []
    for i in range (0,4):
        Eta_new = (GpsEtaChild[i] + 1)/2.0
        GpsEtaChild_new.append(Eta_new)
    
    return GpsEtaChild_new

#%%
    
def get_Xi_Eta_Coordinates (Integ_Input_list, Elem_num): 
    """
    This function maps integration points from the leaf's local coordinate system to the parent
    Iso-parametric element
    
    Quadtree is a list of all leaves within a cut cell
    
       Data structure -> Quadtree (n,2)
       n -> number of leaf nodes
       
       Column 1 ->list- Leaf label-> label format -> [4,2,1]
       where :
       4 ->  parent node in level 1
       2 ->  parent node in level 2
       1 ->  leaf node in level 2
    
      Column 2 -> list -  In/Out of gauss point for this is leaf ->  [1,0,0,1]
       1 - In
       0 - Out
    
    Input : Intg_Input_list -> The list of all leafs for a given cut-cell with inside outside test performed on them
    Output : List of integration points in Xi,Eta coordinates, weights and alpha value
    
    """    
    
    Epsilon = 0.00001                                                       # Alpha value to be assigned to the inetgration points
    Xi = [-0.57735026919, 0.57735026919, 0.57735026919, -0.57735026919 ]    # Location of Xi co-odinates of GPs
    Eta = [-0.57735026919, -0.57735026919, 0.57735026919, 0.57735026919 ]   # Location of Eta co-odinates of GPs
    weight = [1.0, 1.0, 1.0, 1.0]           # Weights for the integration points with respect to leaf's coordinates
    NoLeafs = len(Integ_Input_list)
    Det_Jacobian = 1.0/4.0                  # Determinant of Jacobian for mapping from one level to next level
    
    Integration_Pts = []                    # Empty list of Integration points
    X = []
    Y = []
    W = []
    Alpha = []
    
    #Looping over all the leaves of a cut cell
    for i in range (0,NoLeafs):
        
        weight = [1.0, 1.0, 1.0, 1.0]
        GpXi = 0.0
        GpEta = 0.0
        w = 0.0
        a = 0.0
        ParentID = []                        #ParentID = 0 stands for the main iso-paramteric element
        ChildID = []
        ParentID.append(0)
        Leaf = Integ_Input_list [i]
        depth = len(Leaf[0])
        
        if depth == 1:
            ChildID.append(Integ_Input_list[i][0][0])
        else :
            for j in range (0,depth-1):
                ParentID.append(Integ_Input_list[i][0][j])
            ChildID.append(Integ_Input_list[i][0][depth-1])
        
       
        GpsXiChild = Xi
        GpsEtaChild = Eta
        tempchildID = ChildID[0]
        weighttemp = weight
        m = len(ParentID)-1
        
        while tempchildID != 0:
                          
            if tempchildID ==1:                             #Check for Quadrant 1
                GpsXiChildtemp = XiMap1(GpsXiChild)
                GpsEtaChildtemp = EtaMap1(GpsEtaChild)
            
            elif tempchildID ==2:                           #Check for Quadrant 2
                GpsXiChildtemp = XiMap2(GpsXiChild)
                GpsEtaChildtemp = EtaMap2(GpsEtaChild)
                
            elif tempchildID ==3:                           #Check for Quadrant 3
                GpsXiChildtemp = XiMap3(GpsXiChild)
                GpsEtaChildtemp = EtaMap3(GpsEtaChild)
            
            elif tempchildID ==4:                           #Check for Quadrant 4
                GpsXiChildtemp = XiMap4(GpsXiChild)
                GpsEtaChildtemp = EtaMap4(GpsEtaChild)
            
            #Computation of weights for each integration point
            weight[0] = weighttemp[0]*Det_Jacobian
            weight[1] = weighttemp[1]*Det_Jacobian
            weight[2] = weighttemp[2]*Det_Jacobian
            weight[3] = weighttemp[3]*Det_Jacobian
            
            GpsXiChild = GpsXiChildtemp
            GpsEtaChild = GpsEtaChildtemp
            weight = weighttemp      
            
            tempchildID = ParentID[m]
            m = m-1
        #Loop over the 4 integration points for each leaf within a cut element
        for n in range (0,4):
            GpSet = []
            
            #Check for inside/Outside
            if Integ_Input_list[i][1][n] != 0 :             
                
                a = 1.0
            else:
                a= Epsilon
                
            GpXi = GpsXiChild [n]
            GpEta = GpsEtaChild [n]
            w = weight[n]
            GpSet = [GpXi,GpEta,w,a]          # Each integration point is a list
            X.append(GpXi)
            Y.append(GpEta)
            W.append(w)
            Alpha.append(a)
            Integration_Pts.append(GpSet)

    """
    Uncomment the following line to visualize the inegration point is Xi-Eta coordinates for each leaf
    """
#            if a==1:     
#                pyplot.plot(GpXi,GpEta, 'o', color = 'green')
#            else:
#                pyplot.plot(GpXi,GpEta, 'o', color = 'red')
#
#    pyplot.figure()
  
    return Integration_Pts          
    