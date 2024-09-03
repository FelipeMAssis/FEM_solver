import numpy as np
import matplotlib.pyplot as plt

class Model:
    def __init__(self,nodes=[],materials=[],properties=[],elements=[],loads=[],constraints=[],name='MyModel'):
        self.nodes = nodes
        self.materials = materials
        self.properties = properties
        self.elements = elements
        self.loads = loads
        self.constraints = constraints
        self.name = name
        self.K = None
        self.F = None
        self.q = None

    def assign_global_dof(self):
        global_dof = 0
        for node in self.nodes:
            for dof in range(node.dof):
                node.global_dof[dof] = global_dof
                global_dof+=1
        self.K = np.zeros([global_dof, global_dof])
        self.F = np.nan*np.ones([global_dof,1])
        self.q = np.nan*np.ones([global_dof,1])

    def assemble_stiffness_matrix(self):
        for element in self.elements:
            dofs = []
            for node in element.nodes:
                for dof in node.global_dof:
                    dofs.append(dof)
            for i,dof1 in enumerate(dofs):
                for j,dof2 in enumerate(dofs):
                    self.K[dof1][dof2] = self.K[dof1][dof2]+element.K_global_coord[i][j]
    def assemble_displacements_vector(self):
        for constraint in self.constraints:
            node = self.nodes[constraint.node]
            dof = node.global_dof[constraint.dof]
            self.q[dof] = constraint.value

    def assemble_force_vector(self):
        self.F[np.isnan(self.q)] = 0
        for load in self.loads:
            node = self.nodes[load.node]
            dof = node.global_dof[load.dof]
            self.F[dof] = load.value

    def solve(self):
        dof_red = np.where(np.isnan(self.q))[0]
        F_red = self.F[dof_red]
        K_red = self.K[dof_red][:,1*dof_red]
        q_red = np.linalg.solve(K_red,F_red)
        for i,dof in enumerate(dof_red):
            self.q[dof] = q_red[i]
        self.F = np.dot(self.K,self.q)

    def calculate_dpositions(self):
        for node in self.nodes:
            node.dposition[0] = self.q[node.global_dof[0]]
            node.dposition[1] = self.q[node.global_dof[1]]

    def get_positions(self):
        XX = []
        YY = []
        dXX = []
        dYY = []
        for element in self.elements:
            xx = []
            yy = []
            dxx = []
            dyy = []
            for node in element.nodes:
                xx.append(node.position[0])
                yy.append(node.position[1])
                dxx.append(node.dposition[0])
                dyy.append(node.dposition[1])
            XX.append(xx)
            YY.append(yy)
            dXX.append(dxx)
            dYY.append(dyy)
        return XX, YY, dXX, dYY
    
    def plot(self,factor=0):
        plt.figure()
        XX, YY, dXX, dYY = self.get_positions()
        for xx, yy, dxx, dyy in zip(XX,YY,dXX,dYY):
            plt.plot(xx,yy,':',color='gray')
            plt.plot([x+factor*dx for x,dx in zip(xx,dxx)],[y+factor*dy for y,dy in zip(yy,dyy)],color='blue')
        plt.show()

    def __repr__(self):
        return f'''Model: {self.name}\n
        *N nodes={len(self.nodes)}\n
        *N elements={len(self.elements)}\n
        '''

    