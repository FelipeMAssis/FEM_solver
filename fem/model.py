class Model:
    def __init__(self,nodes=[],materials=[],properties=[],elements=[],loads=[],constraints=[],name='MyModel'):
        self.nodes = nodes
        self.materials = materials
        self.properties = properties
        self.elements = elements
        self.loads = loads
        self.constraints = constraints
        self.name = name
        self.stiffness_matrix = None
        self.force_vector = None
        self.displacements_vector = None
        