class Node:
    def __init__(self, node_id, position, dof=2):
        """
        Initialize a Node.
        
        :param node_id: Unique identifier for the node.
        :param position: Position of the node in the coordinate system (e.g., [x, y, z]).
        :param dof: Degrees of freedom at the node (default is 2 for 2D problems).
        """
        self.node_id = node_id
        self.position = position
        self.dof = dof
        self.displacement = [0.0] * dof
        self.force = [None] * dof
        self.global_dof = [None] * dof

    def __repr__(self):
        return f"Node(id={self.node_id}, pos={self.position}, dof={self.dof})"

