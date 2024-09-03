class Node:
    def __init__(self, node_id, position, dof=2):
        """
        Initialize a Node.
        
        :param node_id: Unique identifier for the node.
        :param position: Position of the node in the coordinate system (e.g., [x, y, z]).
        :param dof: Degrees of freedom at the node (default is 1 for 1D problems).
        """
        self.node_id = node_id
        self.position = position
        self.dof = dof
        self.displacement = [0.0] * dof  # Displacement vector initialized to zero
        self.force = [0.0] * dof         # Force vector initialized to zero
        self.boundary_conditions = [None] * dof  # None indicates no BC applied
        self.global_dof = [None] * dof

    def apply_force(self, force):
        """
        Apply force at the node.
        
        :param force: List of force components corresponding to the degrees of freedom.
        """
        for i in range(len(force)):
            self.force[i] += force[i]

    def set_boundary_condition(self, bc, dof_index):
        """
        Apply a boundary condition to a specific degree of freedom.
        
        :param bc: Value of the boundary condition (e.g., 0 for a fixed boundary).
        :param dof_index: Index of the degree of freedom to which the BC is applied.
        """
        self.boundary_conditions[dof_index] = bc

    def __repr__(self):
        return f"Node(id={self.node_id}, pos={self.position}, dof={self.dof})"
