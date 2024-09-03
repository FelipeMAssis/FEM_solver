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
        self.local_displacement = None
        
        self.length = self.calculate_length()
        self.theta = self.calculate_rotation()

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
    
    def get_local_displacement(self):
        xivec = np.linspace(0,1,100)
        disp = get
        return u

    def __repr__(self):
        return f"Element(id={self.element_id}, nodes={[n.node_id for n in self.nodes]}, length={self.length:.2f}, rotation={np.degrees(self.theta):.2f}°)"

class RodElement(Element):
    def __init__(self, element_id, nodes, property):
        Element.__init__(self, element_id, nodes, property)
        self.T = self.calculate_rotation_matrix()
        self.K = self.calculate_stiffness_matrix()
        self.K_global_coord = self.T.T @ self.K @ self.T
    
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
    
    def get_local_displacement(self):
        disp = []
        for node in self.nodes:
            disp = disp + node.displacement
        self.local_displacement = self.T @ np.array([disp]).T
          
class BarElement(Element):
    def __init__(self, element_id, nodes, property):
        Element.__init__(self, element_id, nodes, property)
        self.T = self.calculate_rotation_matrix()
        self.K = self.calculate_stiffness_matrix()
        self.K_global_coord = self.T.T @ self.K @ self.T

    def calculate_rotation_matrix(self):
        """
        Calculate the rotation matrix for the element.
        """
        cos_theta = np.cos(self.theta)
        sin_theta = np.sin(self.theta)
        return np.array([[cos_theta, -sin_theta, 0, 0, 0, 0],
                         [sin_theta, cos_theta, 0, 0, 0, 0],
                         [0, 0, 1, 0, 0, 0],
                         [0, 0, 0, cos_theta, -sin_theta, 0],
                         [0, 0, 0, sin_theta, cos_theta, 0],
                         [0, 0, 0, 0, 0, 1]])

    def calculate_stiffness_matrix(self):
        """
        Calculate the local stiffness matrix for the element.
        (Assuming a 2D bar element with 2 nodes)
        """
        E = self.property.material.youngs_modulus
        L = self.length
        A = self.property.area
        Izz = self.property.Izz

        k0 = (E * A) / L
        k1 = (E * Izz) / L
        k2 = (E * Izz) / L**2
        k3 = (E * Izz) / L**3

        # 2x2 stiffness matrix for a 1D rod element
        return np.array([[k0, 0, 0, -k0, 0, 0],
                        [0, 12*k3, 6*k2, 0, -12*k3, 6*k2],
                        [0, 6*k2, 4*k1, 0, -6*k2, 2*k1],
                        [-k0, 0, 0, k0, 0, 0],
                        [0, -12*k3, -6*k2, 0, 12*k3, -6*k2],
                        [0, 6*k2, 2*k1, 0, -6*k2, 4*k1]])

