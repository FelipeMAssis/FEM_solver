class NodalConstraint:
    def __init__(self,node,dof,value):
        self.node = node
        self.dof = dof
        self.value = value
    def __repr__(self):
        return f"Nodal constraint(node={self.node}, dof={self.dof}, value={self.value})"
