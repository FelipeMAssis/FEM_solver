class NodalLoad:
    def __init__(self,node,dof,value):
        self.node = node
        self.dof = dof
        self.value = value