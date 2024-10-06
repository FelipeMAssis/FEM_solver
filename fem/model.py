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

    def assign_global_dof(self):
        """
        Assign global degrees of freedom (DOF) to each node and initialize matrices.
        """
        global_dof = 0
        for node in self.nodes:
            for dof in range(node.dof):
                node.global_dof[dof] = global_dof
                global_dof += 1
        
        self.K = np.zeros((global_dof, global_dof))
        self.F = np.full((global_dof, 1), np.nan)
        self.q = np.full((global_dof, 1), np.nan)

    def assemble_stiffness_matrix(self):
        """
        Assemble the global stiffness matrix by summing element stiffness matrices.
        """
        for element in self.elements:
            dofs = [dof for node in element.nodes for dof in node.global_dof]
            for i, dof1 in enumerate(dofs):
                for j, dof2 in enumerate(dofs):
                    self.K[dof1, dof2] += element.K_global_coord[i, j]

    def assemble_displacements_vector(self):
        """
        Assemble the global displacement vector based on constraints.
        """
        for constraint in self.constraints:
            node = self.nodes[constraint.node]
            dof = node.global_dof[constraint.dof]
            self.q[dof] = constraint.value

    def assemble_force_vector(self):
        """
        Assemble the global force vector based on applied loads.
        """
        self.F[np.isnan(self.q)] = 0
        for load in self.loads:
            node = self.nodes[load.node]
            dof = node.global_dof[load.dof]
            self.F[dof] = load.value

    def solve_eqs(self):
        """
        Solve for the unknown displacements using the reduced system of equations.
        """
        dof_red = np.where(np.isnan(self.q))[0]
        F_red = self.F[dof_red]
        K_red = self.K[np.ix_(dof_red, dof_red)]
        q_red = np.linalg.solve(K_red, F_red)
        
        for i, dof in enumerate(dof_red):
            self.q[dof] = q_red[i]
        
        self.F = np.dot(self.K, self.q)
    
    def solve(self):
        self.assign_global_dof()
        self.assemble_stiffness_matrix()
        self.assemble_displacements_vector()
        self.assemble_force_vector()
        self.solve_eqs()
        return Output(self)

