import numpy as np

class Element:
    def __init__(self, element_id, nodes, property):
        """
        Initialize an Element.
        
        :param element_id: Unique identifier for the element.
        :param nodes: List of Node objects that form the element.
        :param property: Property object.
        """
        self.element_id = element_id
        self.nodes = nodes
        self.property = property
        
        self.length = self.calculate_length()
        self.theta = self.calculate_rotation()
        self.T = self.calculate_rotation_matrix()
        self.K = self.calculate_stiffness_matrix()
        self.K_global_coord = self.T.T @ self.K @ self.T

    def calculate_length(self):
        """
        Calculate the length of the element (assuming 2D for simplicity).
        """
        x0, y0 = self.nodes[0].position
        x1, y1 = self.nodes[1].position
        return np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
    
    def calculate_rotation(self):
        """
        Calculate the rotation angle of the element (assuming 2D for simplicity).
        """
        x0, y0 = self.nodes[0].position
        x1, y1 = self.nodes[1].position
        return np.arctan2(y1 - y0, x1 - x0)
    
    def calculate_rotation_matrix(self):
        """
        Calculate the rotation matrix for the element.
        """
        cos_theta = np.cos(self.theta)
        sin_theta = np.sin(self.theta)
        return np.array([[cos_theta, sin_theta, 0, 0],
                         [0, 0, cos_theta, sin_theta]])

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
        return k * np.array([[1, -1],
                             [-1, 1]])

    def __repr__(self):
        return f"Element(id={self.element_id}, nodes={[n.node_id for n in self.nodes]}, length={self.length:.2f}, rotation={np.degrees(self.theta):.2f}°)"
