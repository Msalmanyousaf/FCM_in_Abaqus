# -*- coding: utf-8 -*-

#%%
import numpy as np
import numpy.linalg as la
#%%

class Cut_Element_Integration:

    def __init__(self, nodal_coordinates, E, t, prxy,Integration_points):
        self._nodal_coordinates = nodal_coordinates
        self._E = E
        self._t = t
        self._prxy = prxy
        self.Xi_points = []
        self.Eta_points = []
        self.Weights = []
        
        for i in range (0,len(Integration_points)):
            self.Xi_points.append(Integration_points[i][0])
            self.Eta_points.append(Integration_points[i][1])
            self.Weights.append(Integration_points[i][2])



    def calculate_elastic_stiffness_matrix(self):
        """
        This function calculate Stiffness Matrix for the cut element
        
        Input: : Cut element
        Output : Cut element stiffness matrix
        """

        K_e = np.zeros((8,8))

        C = self._comp_mat_matrix_plane_stress()

        for i in range(len(self.Eta_points)):
            ip_xi = self.Xi_points[i]      #current Integration point's xi coordinate 
            ip_eta = self.Eta_points[i]    #current Integration point's eta coordinate 
            ip_w = self.Weights[i]         #current Integration point's weight


            # Jacobian, inverse and determinant
            J = self._calculate_Jacobian(ip_xi, ip_eta)
            J_inv = la.inv(J)
            det_J = la.det(J)

            # B-matrix
            B = self._calculate_B_matrix(ip_xi, ip_eta, J_inv)

                ##Sum up over all GPs
            K_e += (np.dot(np.dot(B.T, C) ,B)) * det_J *ip_w

        ## multiply with thickness
        K_e *= self._t
        
        return K_e
    

    def _comp_mat_matrix_plane_stress(self):
        """
        This function calculates the elasticity tensor of an isotropic material
        with plane stress condition
        
        Input: Cut element
        Output : Elasticity Tensor C
        """
        E = self._E
        prxy = self._prxy
        C = np.matrix([ [1,    prxy, 0         ],
                        [prxy, 1,    0         ],
                        [0,    0,    (1-prxy)/2] ])
        C *= E / (1 - prxy**2)
        return C

    
    def _calculate_B_matrix(self, xi, eta, J_inv):
        """
        This function calculates the strain displacement matrix (B) for a cut element

        Input: Xi and Eta coordinates of the integration point, inverse of the jacobian matrix
        Output: B matrix
        
        """
        
        ## calculate B matrix
        B = np.zeros((3,8))      #initialize B
        dN_dxi_deta = self.calculate_shapefunctions_derivatives(xi, eta)
        dN_dx_dy = np.dot(J_inv, dN_dxi_deta)
        ## The Definition of B has changed to fit abaqus definition "DOFS (5,7)&(6,8) are interchanged"
        for j in range(4):
            B[0,j*2+0] = dN_dx_dy[0,j]
            B[0,j*2+1] = 0
            B[1,j*2+0] = 0
            B[1,j*2+1] = dN_dx_dy[1,j]
            B[2,j*2+0] = dN_dx_dy[1,j]
            B[2,j*2+1] = dN_dx_dy[0,j]
        
        return B
    

    def calculate_shapefunctions_derivatives(self, xi ,eta):
        """
        This function calculates the derivative of the bilinear shape function with respect to
        cut element's paremetric coordinates

        Input: Xi and Eta coordinates of the integration point
        Output : dN
                    [[dN1_dxi,  dN2_dxi,  dN3_dxi,  dN4_dxi],
                     [dN1_deta, dN2_deta, dN3_deta, dN4_deta]]
 
        """
        
        #w.r.t xi
        dN1_dxi = ((-1)*(1-eta))/4  #shapefunction node 1
        dN2_dxi = (( 1)*(1-eta))/4  #shapefunction node 2
        dN3_dxi = (( 1)*(1+eta))/4  #shapefunction node 3
        dN4_dxi = ((-1)*(1+eta))/4  #shapefunction node 4
        #w.r.t eta
        dN1_deta = ((1-xi)*(-1))/4  #shapefunction node 1
        dN2_deta = ((1+xi)*(-1))/4  #shapefunction node 2
        dN3_deta = ((1+xi)*( 1))/4  #shapefunction node 3
        dN4_deta = ((1-xi)*( 1))/4  #shapefunction node 4

        dN = np.matrix([[dN1_dxi,  dN2_dxi,  dN3_dxi,  dN4_dxi],
                        [dN1_deta, dN2_deta, dN3_deta, dN4_deta]])
        return dN
    

    def _calculate_Jacobian(self, xi, eta):
        """
        This function calculates the Jacobian of the cut element
        
        
        Input: Xi and Eta coordinates of the integration point
        Output : The jacobian matrix
        """
        
        nodal_coordinates = self._nodal_coordinates
        dN_dxi_deta = self.calculate_shapefunctions_derivatives(xi, eta)
        J = np.dot(dN_dxi_deta, nodal_coordinates)
        return J
