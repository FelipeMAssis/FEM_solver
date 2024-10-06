import numpy as np
from fem.output import Output

class Model:
    def __init__(self, nodes=None, materials=None, properties=None, elements=None, loads=None, constraints=None, name='MyModel'):
        """
        Initialize the finite element model.

        :param nodes: List of Node objects.
        :param materials: List of Material objects.
        :param properties: List of Property objects.
        :param elements: List of Element objects.
        :param loads: List of NodalLoad objects.
        :param constraints: List of NodalConstraint objects.
        :param name: Name of the model.
        """
        self.nodes = nodes or []
        self.materials = materials or []
        self.properties = properties or []
        self.elements = elements or []
        self.loads = loads or []
        self.constraints = constraints or []
        self.name = name

        self.K = None  # Global stiffness matrix
        self.F = None  # Global force vector
        self.q = None  # Global displacement vector

    def assign_global_dof(self):
        """
        Assign global degrees of freedom (DOF) to each node and initialize global matrices.
        """
        global_dof = 0
        for node in self.nodes:
            node.global_dof = [global_dof + i for i in range(node.dof)]
            global_dof += node.dof
        
        self._initialize_global_matrices(global_dof)

    def _initialize_global_matrices(self, size):
        """
        Initialize the global stiffness, force, and displacement matrices.

        :param size: Total number of global degrees of freedom.
        """
        self.K = np.zeros((size, size))  # Global stiffness matrix
        self.F = np.full((size, 1), np.nan)  # Global force vector
        self.q = np.full((size, 1), np.nan)  # Global displacement vector

    def assemble_stiffness_matrix(self):
        """
        Assemble the global stiffness matrix by summing element stiffness matrices.
        """
        for element in self.elements:
            element_dofs = self._get_element_dofs(element)
            self._add_element_stiffness_to_global(element, element_dofs)

    def _get_element_dofs(self, element):
        """
        Get the global DOFs for the nodes of an element.

        :param element: Element object.
        :return: List of global DOFs.
        """
        return [dof for node in element.nodes for dof in node.global_dof]

    def _add_element_stiffness_to_global(self, element, dofs):
        """
        Add the element stiffness matrix to the global stiffness matrix.

        :param element: Element object.
        :param dofs: Global DOFs associated with the element.
        """
        for i, dof1 in enumerate(dofs):
            for j, dof2 in enumerate(dofs):
                self.K[dof1, dof2] += element.K_global_coord[i, j]

    def assemble_displacements_vector(self):
        """
        Assemble the global displacement vector based on nodal constraints.
        """
        for constraint in self.constraints:
            node = self.nodes[constraint.node]
            self.q[node.global_dof[constraint.dof]] = constraint.value

    def assemble_force_vector(self):
        """
        Assemble the global force vector based on applied loads.
        """
        # Set force to zero where displacements are prescribed
        self.F[np.isnan(self.q)] = 0  
        
        for load in self.loads:
            node = self.nodes[load.node]
            self.F[node.global_dof[load.dof]] = load.value

    def solve_eqs(self):
        """
        Solve for the unknown displacements using the reduced system of equations.
        """
        dof_free = np.isnan(self.q).flatten()  # Indices of free DOFs
        K_reduced = self.K[dof_free][:, dof_free]  # Reduced stiffness matrix
        F_reduced = self.F[dof_free]  # Reduced force vector
        
        q_reduced = np.linalg.solve(K_reduced, F_reduced)  # Solve for unknown displacements
        
        self.q[dof_free] = q_reduced.reshape(-1, 1)  # Update displacement vector
        self.F = np.dot(self.K, self.q)  # Update the force vector for all DOFs

    def solve(self):
        """
        Main function to solve the finite element model.
        It assembles the global matrices and solves for displacements.
        
        :return: Output object containing results of the solved model.
        """
        self.assign_global_dof()
        self.assemble_stiffness_matrix()
        self.assemble_displacements_vector()
        self.assemble_force_vector()
        self.solve_eqs()

        return Output(self)


