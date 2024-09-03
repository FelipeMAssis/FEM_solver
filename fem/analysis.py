import numpy as np

class Analysis:
    def __init__(self, model):
        self.model = model
    def assign_global_dof(self):
        global_dof = 0
        for node in self.model.nodes:
            for dof in range(node.dof):
                node.global_dof[dof] = global_dof
                global_dof+=1
        self.model.stiffness_matrix = np.zeros([global_dof, global_dof])
        self.model.force_vector = np.zeros([1, global_dof])
        self.model.displacements = np.zeros([1, global_dof])
    def assemble_stiffness_matrix(self):
        pass