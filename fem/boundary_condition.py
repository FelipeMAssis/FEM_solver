class NodalConstraint:
    def __init__(self, node, dof, value):
        """
        Initialize a NodalConstraint.
        
        :param node: The Node object where the constraint is applied.
        :param dof: The degree of freedom at which the constraint is applied.
        :param value: The value of the constraint (e.g., displacement or rotation).
        """
        self.node = node
        self.dof = dof
        self.value = value

    def __repr__(self):
        return f"NodalConstraint(node={self.node.node_id}, dof={self.dof}, value={self.value})"


class NodalLoad:
    def __init__(self, node, dof, value):
        """
        Initialize a NodalLoad.
        
        :param node: The Node object where the load is applied.
        :param dof: The degree of freedom at which the load is applied.
        :param value: The magnitude of the load.
        """
        self.node = node
        self.dof = dof
        self.value = value

    def __repr__(self):
        return f"NodalLoad(node={self.node.node_id}, dof={self.dof}, value={self.value})"
