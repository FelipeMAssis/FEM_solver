import numpy as np

class Element:
    element_count = 0

    def __init__(self, nodes, property):
        """
        Initialize an Element.
        
        :param nodes: List of nodes that define the element.
        :param property: Property of the element, which includes material properties.
        """
        self.id = Element.element_count
        Element.element_count += 1
        self.nodes = nodes
        self.property = property

    def rotate_K(self):
        """
        Rotate the local stiffness matrix to global coordinates.
        """
        return self.T.T @ self.K @ self.T

    def __repr__(self):
        return f'Element:\n ID = {self.id}\n Nodes = {[n.id for n in self.nodes]}\n Property = {self.property.id}\n'


class Element2DLine(Element):
    def __init__(self, nodes, property):
        """
        Initialize a 2D Line Element.
        
        :param nodes: List of nodes that define the element.
        :param property: Property of the element, which includes material properties.
        """
        super().__init__(nodes, property)
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


class ElementRod(Element2DLine):
    def __init__(self, nodes, property):
        """
        Initialize a 2D Rod Element.
        
        :param nodes: List of nodes that define the element.
        :param property: Property of the rod element, which includes material properties.
        """
        super().__init__(nodes, property)
        for node in nodes:
            node.assign_dof(2)
        self.T = self.calculate_rotation_matrix()
        self.K = self.calculate_stiffness_matrix()
        self.K_global_coord = self.rotate_K()

    def calculate_rotation_matrix(self):
        """
        Calculate the transformation matrix for the rod element.
        """
        cos_theta = np.cos(self.theta)
        sin_theta = np.sin(self.theta)
        return np.array(
            [[cos_theta, sin_theta, 0, 0],
            [0, 0, cos_theta, sin_theta]]
        )

    def calculate_stiffness_matrix(self):
        """
        Calculate the local stiffness matrix for the rod element.
        """
        E = self.property.material.youngs_modulus
        L = self.length
        A = self.property.area

        k = (E * A) / L

        # 2x2 stiffness matrix for a 1D rod element
        return k * np.array(
            [[1, -1],
            [-1, 1]]
        )

    def calculate_local_results(self):
        """
        Calculate the local deformation and force results for the rod element.
        """
        q_global = np.array(self.nodes[0].displacement + self.nodes[1].displacement)
        q_local = self.T @ q_global
        E = self.property.material.youngs_modulus
        A = self.property.area
        L = self.length
        self.deformation = (q_local[1] - q_local[0])
        self.force = E * A * self.deformation / L


class ElementBeam(Element2DLine):
    def __init__(self, nodes, property):
        """
        Initialize a 2D Beam Element.
        
        :param nodes: List of nodes that define the element.
        :param property: Property of the beam element, which includes material properties.
        """
        super().__init__(nodes, property)
        for node in nodes:
            node.assign_dof(3)
        self.T = self.calculate_rotation_matrix()
        self.K = self.calculate_stiffness_matrix()
        self.K_global_coord = self.rotate_K()

    def calculate_rotation_matrix(self):
        """
        Calculate the transformation matrix for the beam element.
        """
        cos_theta = np.cos(self.theta)
        sin_theta = np.sin(self.theta)
        return np.array(
            [[cos_theta, sin_theta, 0, 0, 0, 0],
            [-sin_theta, cos_theta, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, cos_theta, sin_theta, 0],
            [0, 0, 0, -sin_theta, cos_theta, 0],
            [0, 0, 0, 0, 0, 1]]
        )

    def calculate_stiffness_matrix(self):
        """
        Calculate the local stiffness matrix for the beam element.
        """
        E = self.property.material.youngs_modulus
        L = self.length
        A = self.property.area
        Izz = self.property.Izz

        k0 = (E * A) / L
        k1 = (E * Izz) / L
        k2 = (E * Izz) / L**2
        k3 = (E * Izz) / L**3

        # 6x6 stiffness matrix for a beam element
        return np.array(
            [[k0, 0, 0, -k0, 0, 0],
            [0, 12*k3, 6*k2, 0, -12*k3, 6*k2],
            [0, 6*k2, 4*k1, 0, -6*k2, 2*k1],
            [-k0, 0, 0, k0, 0, 0],
            [0, -12*k3, -6*k2, 0, 12*k3, -6*k2],
            [0, 6*k2, 2*k1, 0, -6*k2, 4*k1]]
        )

    def calculate_local_results(self):
        """
        Calculate the local deformation and force results for the beam element.
        """
        q_global = np.array(self.nodes[0].displacement + self.nodes[1].displacement)
        q_local = self.T @ q_global
        self.axialdeform = (q_local[4] - q_local[0])
        self.transvdeform = None
        self.axialFmean = None
        self.bendingSmean = None
        self.bendingMmean = None

import numpy as np

class ElementCST(Element):
    def __init__(self, nodes, property):
        """
        Initialize a Constant Strain Triangle (CST) element.

        :param nodes: List of 3 nodes defining the triangular element.
        :param property: Property object defining material and geometric properties of the element.
        """
        super().__init__(nodes, property)
        for node in nodes:
            node.assign_dof(2)  # CST elements typically have 2 degrees of freedom per node
        self.area = self.calculate_area()
        self.K_global_coord = self.calculate_stiffness_matrix()

    def calculate_area(self):
        """
        Calculate the area of the triangular element using the determinant method.

        :return: Area of the triangle.
        """
        x1, y1 = self.nodes[0].position
        x2, y2 = self.nodes[1].position
        x3, y3 = self.nodes[2].position
        
        # Matrix representation for area calculation
        area_matrix = np.array([[1, x1, y1],
                                [1, x2, y2],
                                [1, x3, y3]])
        
        # Determinant of the area matrix divided by 2
        return np.abs(np.linalg.det(area_matrix)) / 2

    def calculate_stiffness_matrix(self):
        """
        Calculate the global stiffness matrix for the CST element.

        :return: Global stiffness matrix for the CST element.
        """
        x1, y1 = self.nodes[0].position
        x2, y2 = self.nodes[1].position
        x3, y3 = self.nodes[2].position
        A = self.area

        # Strain-displacement matrix (B-matrix)
        B = (1 / (2 * A)) * np.array([[y2 - y3, 0, y3 - y1, 0, y1 - y2, 0],
                                      [0, x3 - x2, 0, x1 - x3, 0, x2 - x1],
                                      [x3 - x2, y2 - y3, x1 - x3, y3 - y1, x2 - x1, y1 - y2]])

        # Material properties (D-matrix)
        E = self.property.material.youngs_modulus
        nu = self.property.material.poissons_ratio
        
        # Modify for plane strain condition
        if not self.property.plane_stress:
            E /= (1 - nu ** 2)
            nu /= (1 - nu ** 2)
        
        # Elasticity matrix (D-matrix)
        D = (E / (1 - nu ** 2)) * np.array([[1, nu, 0],
                                            [nu, 1, 0],
                                            [0, 0, (1 - nu) / 2]])

        # Element stiffness matrix in global coordinates
        t = self.property.thickness
        return (A * t) * (B.T @ D @ B)

    def __repr__(self):
        """
        String representation of the CST element.
        """
        return (f"ElementCST:\n ID = {self.id}\n Nodes = {[node.id for node in self.nodes]}\n"
                f"Area = {self.area:.4f}\n")
