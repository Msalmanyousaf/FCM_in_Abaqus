# Implementation of Finite Cell Method (FCM) in Abaqus  
In this project, Finite Cell Method (FCM) is implemented in Abaqus for 2D plane stress problems.

## 1. Finite Element Method (FEM)
Abaqus is a well-known commercial software which uses Finite Element Method (FEM) to simulate various engineering-related problems (e.g. general stress analysis, structural analysis etc.). The usual procedure starts with making a CAD model of the structure which you want to analyse. Then, this CAD geometry is discretized into finite number of small elements. Now, the geometry is completely described by this finite element mesh. If the size of the elements is small enough, the details of the geometry are resolved in a better way. After the discretization step, boundary conditions are applied and the partial differential equations are solved numerically to get the resulting stresses and displacements.  Important point is that the finite element mesh conforms to the geometry. No element is allowed to cut the boundary of the geometry.    

## 2. Finite Cell Method (FCM)
The above mentioned technique based on FEM is quite powerful in simulating many real world problems. However, if we have a very complicated geometry, the discretization step can be very challenging. The resulting elements will suffer from the problems of distortion, negative Jacobian and other mesh-related issues.  

To solve the above issues, research is being done on a relatively advanced technique known as Finite Cell Method (FCM). Here, we do not discretize the geometry directly, rather, a structured gird is generated and the geometry is imposed on it. So, the discretized "cells" do not conform the geometry i.e. they may even cut the boundary of the geometry. Now, the grid is refined just around the boundary using quadtree algorithm.   

The cells which cut the boundary require special treatment. Adaptive integration is used to find the stiffness matrix of these cells. Moreover, UEL (User Element Subroutine) is used to assign the computed stiffness matrix to these cells.  

For complete description of the project, please refer to the file "Project_description".