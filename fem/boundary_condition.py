constraint_count = 0
load_count = 0

class NodalConstraint:
    def __init__(self, node, dof, value):
        """
        Initialize a NodalConstraint.
        
        :param node: The Node object where the constraint is applied.
        :param dof: The degree of freedom at which the constraint is applied.
        :param value: The value of the constraint (e.g., displacement or rotation).
        """
        global constraint_count
        self.id = constraint_count
        constraint_count = constraint_count + 1
        self.node = node
        self.dof = dof
        self.value = value

    def __repr__(self):
        return f"NodalConstraint:\n ID = {self.id}\n Node = {self.node}\n DOF = {self.dof}\n Value = {self.value}"


class NodalLoad:
    def __init__(self, node, dof, value):
        """
        Initialize a NodalLoad.
        
        :param node: The Node object where the load is applied.
        :param dof: The degree of freedom at which the load is applied.
        :param value: The magnitude of the load.
        """
        global load_count
        self.id = load_count
        load_count = load_count + 1
        self.node = node
        self.dof = dof
        self.value = value

    def __repr__(self):
        return f"NodalLoad:\n ID = {self.id}\n Node = {self.node}\n DOF = {self.dof}\n Value = {self.value}"
