import numpy as np

class Element:
    def __init__(self, element_id, nodes, property):
        """
        Initialize an Element.
        
        :param element_id: Unique identifier for the element.
        :param nodes: List of Node objects that form the element.
        :param material: Property object.
        """
        self.element_id = element_id
        self.nodes = nodes
        self.property = property
        self.length = self.calculate_length()
        self.theta = self.calculate_rotation()
        self.T = self.calculate_rotation_matrix()
        self.K = self.calculate_stiffness_matrix()
        self.K_global_coord = np.dot(self.T.transpose(),np.dot(self.K,self.T))

    def calculate_length(self):
        """
        Calculate the length of the element (assuming 2D for simplicity).
        """
        return np.sqrt(
            (self.nodes[1].position[0] - self.nodes[0].position[0])**2 + 
            (self.nodes[1].position[1] - self.nodes[0].position[1])**2
        )
    
    def calculate_rotation(self):
        """
        Calculate the rotation of the element (assuming 2D for simplicity).
        """
        if self.nodes[1].position[0]>self.nodes[0].position[0] and self.nodes[1].position[1]>=self.nodes[0].position[1]: # 1st quadrant
            return np.arctan(
                (self.nodes[1].position[1] - self.nodes[0].position[1])/
                (self.nodes[1].position[0] - self.nodes[0].position[0])
            )
        elif self.nodes[1].position[0]<self.nodes[0].position[0] and self.nodes[1].position[1]>=self.nodes[0].position[1]: # 2nd quadrant
            return np.pi+np.arctan(
                (self.nodes[1].position[1] - self.nodes[0].position[1])/
                (self.nodes[1].position[0] - self.nodes[0].position[0])
            )
        elif self.nodes[1].position[0]<self.nodes[0].position[0] and self.nodes[1].position[1]<=self.nodes[0].position[1]: # 3rd quadrant
            return np.pi+np.arctan(
                (self.nodes[1].position[1] - self.nodes[0].position[1])/
                (self.nodes[1].position[0] - self.nodes[0].position[0])
            )
        elif self.nodes[1].position[0]>self.nodes[0].position[0] and self.nodes[1].position[1]<=self.nodes[0].position[1]: # 4th quadrant
            return 2*np.pi+np.arctan(
                (self.nodes[1].position[1] - self.nodes[0].position[1])/
                (self.nodes[1].position[0] - self.nodes[0].position[0])
            )
        elif self.nodes[1].position[0]==self.nodes[0].position[0] and self.nodes[1].position[1]>self.nodes[0].position[1]: # 90°
            return np.pi/2
        else:
            return np.pi*1.5
        
    def calculate_rotation_matrix(self):
        return np.array([[np.cos(self.theta), np.sin(self.theta), 0, 0],
                         [0, 0, np.cos(self.theta), np.sin(self.theta)]])


    def calculate_stiffness_matrix(self):
        """
        Calculate the local stiffness matrix for the element.
        (Assuming a 1D rod element with 2 nodes)
        """
        E = self.property.material.youngs_modulus
        L = self.length
        A = self.property.area

        k = (E * A) / L

        # 2x2 stiffness matrix for a 1D rod element
        stiffness_matrix = k * np.array([[1, -1],
                                         [-1, 1]])
        return stiffness_matrix

    def __repr__(self):
        return f"Element(id={self.element_id}, nodes={[n.node_id for n in self.nodes]}, length={self.length}, rotation={np.degrees(self.theta)}°)"
