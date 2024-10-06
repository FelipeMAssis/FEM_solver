class Node:
    node_count = 0

    def __init__(self, position):
        """
        Initialize a Node.
        
        :param position: Position of the node in the coordinate system (e.g., [x, y, z]).
        """
        self.id = Node.node_count
        Node.node_count += 1

        self.position = position
        self.dof = None
        self.displacement = None
        self.force = None
        self.global_dof = None

    def assign_dof(self, dof):
        self.dof = dof
        self.displacement = [0.0] * dof
        self.force = [None] * dof
        self.global_dof = [None] * dof

    def __repr__(self):
        description = f"Node:\n ID = {self.id}\n Position = {self.position}\n"
        
        if self.dof is not None:
            description += f" DOF = {self.dof}\n"
        
        return description
