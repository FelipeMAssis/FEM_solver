node_count = 0

class Node:
    def __init__(self, position):
        """
        Initialize a Node.
        
        :param node_id: Unique identifier for the node.
        :param position: Position of the node in the coordinate system (e.g., [x, y, z]).
        :param dof: Degrees of freedom at the node (default is 2 for 2D problems).
        """
        global node_count
        self.id = node_count
        node_count = node_count + 1

        self.position = position
        self.dof = None

    def assign_dof(self,dof):
        self.dof = dof
        self.displacement = [0.0] * dof
        self.force = [None] * dof
        self.global_dof = [None] * dof

    def __repr__(self):
        
        description = f'''Node:\n ID = {self.id}\n Position = {self.position}\n'''
        
        if self.dof!=None:
            return description + ' DOF = {self.dof})\n'
        else:
            return description

