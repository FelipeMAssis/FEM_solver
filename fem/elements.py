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
        self.stiffness_matrix = self.calculate_stiffness_matrix()

    def calculate_length(self):
        """
        Calculate the length of the element (assuming 1D for simplicity).
        """
        return np.sqrt(
            (self.nodes[1].position[0] - self.nodes[0].position[0])**2 + 
            (self.nodes[1].position[1] - self.nodes[0].position[1])**2
        )

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
        return f"Element(id={self.element_id}, nodes={[n.node_id for n in self.nodes]}, length={self.length})"
