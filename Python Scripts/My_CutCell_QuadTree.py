# -*- coding: utf-8 -*-

"""
Each cut element is an instance of the class QuadTree
"""
#%%

from shapely.geometry import box
from matplotlib import pyplot as plt

#%%

Leaves=[]
temp=[]
Label = []

class QuadTree():
    
    """
    Convention is:
        myChildren[0] = SW  myChildren[1] = SE
        myChildren[2] = NE  myChildren[3] = NW
        
    """
    #Nodes and Leaves Counter
    myNoOfNodes = 0
    myNoOfLeaves = 0
    Integ_Input= []
    
    
    def __init__(self,CutCellNum,Phy_domain, xmin, ymin, xmax, ymax, father, level, stringCode,ID):
        self.ElementNum=CutCellNum
        self.Domain=Phy_domain
        self.myXmin = xmin
        self.myYmin = ymin
        self.myXmax = xmax
        self.myYmax = ymax
        self.myfather = father
        self.myLevel = level
        self.myStringCode = stringCode
        self.myChildren = None
        self.myCell = box(xmin, ymin, xmax, ymax)
        self.ID = ID
        self.label = []
        QuadTree.myNoOfNodes+=1
    	       
    
    def divideMe(self):
        """
        This function creates 4 new objects of type Quadtree
        
        Input : The current object
        Output : None
        
        """     
        self.middleX = 0.5 * (self.myXmax + self.myXmin)
        self.middleY = 0.5 * (self.myYmax + self.myYmin)
        self.myChildren = [QuadTree(self.ElementNum, self.Domain,self.myXmin, self.myYmin, self.middleX, self.middleY, self, self.myLevel + 1, "0",1),
                           QuadTree(self.ElementNum, self.Domain,self.middleX, self.myYmin, self.myXmax, self.middleY, self, self.myLevel + 1, "0",2),
                           QuadTree(self.ElementNum, self.Domain,self.middleX, self.middleY, self.myXmax, self.myYmax, self, self.myLevel + 1, "0",3),
                           QuadTree(self.ElementNum, self.Domain,self.myXmin, self.middleY, self.middleX, self.myYmax, self, self.myLevel + 1, "0",4)]               
        for i in range (0,4):
            self.myChildren[i].Integration_Input()    
   
    
    def amIcut(self):
        """
        This function checks whether the current object (cut element's leaf) is cut
        The object's string code is updated as follows
        # 0 = totally outside
        # 1 = totally inside
        # 2 = cut 
        
        Input : The current object
        Output : A Boolen (0 or 1)
        
        """
                       
        if self.Domain.contains(self.myCell):
            self.myStringCode = '1'
            return False
        
        elif self.myCell.intersects(self.Domain):
            self.myStringCode = '2'
            return True
        
        else:
            self.myStringCode = '0'
            return False

           
    def generateQuadtree(self, maxLevel):
        """
        This functions generates quadtree for the cut element recursively till the specified depth
        
        Input : Current Object & The depth to which Quad-tree is to be performed
        Output : None
        
        """  
        if (self.myLevel < maxLevel and self.amIcut()):
            self.divideMe()
            for children in self.myChildren:
                children.generateQuadtree(maxLevel)
                
               
    def Get_myNoOfLeaves(self):
        """
        This function returns number of leaves for a cut element
        
        Input : The cut element object
        Output : Number of leaves for the cut element
        
        """  
        if (self.myChildren!= None):
                for children in self.myChildren:
                    children.Return_Leaves_list()
        else:
            QuadTree.myNoOfLeaves+=1
            
        return QuadTree.myNoOfLeaves
    
            
    def Return_Leaves_list(self):
        """
        This function returns the minimum and maximum bounds for each leaf of a cut element
        
        Input : The cut element object
        Output : A list containing minimum and maximum bounds for each leaf of a cut element
        
        """  
        if(self.myfather==None):
                del Leaves[:]
                
        if (self.myChildren!= None):
            for children in self.myChildren:
                children.Return_Leaves_list()
        else:
            QuadTree.myNoOfLeaves+=1
            temp=[(self.myXmin,self.myYmin),(self.myXmax,self.myYmax)]
            if temp not in Leaves:
                Leaves.append(temp)
                            
        return Leaves
           
        
    def Integration_Input(self):
        
        """
        This function creates the label of each node.
        for e.g, if a node has the following label [4,2,1]. This means:
           4 ->  parent node in level 1
           2 ->  parent node in level 2
           1 ->  node ID in level 2
        
        Input: The current object
        Output: None
        """
        if self.myfather != None:
            for i in range (0,len(self.myfather.label)):
                self.label.append(self.myfather.label[i])
            self.label.append(self.ID)

            
    def Return_Label_list(self, Label):
        """
        This function returns the label for each leaf of a cut element
        for e.g, if a leaf has the following label [4,2,1]. This means:
           4 ->  parent node in level 1
           2 ->  parent node in level 2
           1 ->  leaf node in level 2
        
        Input : The cut element object
        Output : None
        
        """ 
        if(self.myfather==None):
                del Label[:]
        
        if (self.myChildren != None):
             for children in self.myChildren:
                 children.Return_Label_list(Label)
                 if children.myStringCode !='2':
                     temp = children.label
                     Label.append(temp)
                
        
    def plotTreeToConsole(self):
        """
        This function plots the Quad tree of a cut element to console
        
        Input : The cut element object
        Output : None
        
        """ 
        x,y = self.myCell.exterior.xy
        plt.plot(x,y, color='blue',linewidth = 1.0)
        if (self.myChildren != None):
            for children in self.myChildren:
                children.plotTreeToConsole()
            
            
