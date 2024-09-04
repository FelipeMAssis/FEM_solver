import numpy as np
import matplotlib.pyplot as plt

class Model:
    def __init__(self, nodes=None, materials=None, properties=None, elements=None, loads=None, constraints=None, name='MyModel'):
        """
        Initialize the finite element model.
        
        :param nodes: List of Node objects.
        :param materials: List of Material objects.
        :param properties: List of Property objects.
        :param elements: List of Element objects.
        :param loads: List of NodalLoad objects.
        :param constraints: List of NodalConstraint objects.
        :param name: Name of the model.
        """
        self.nodes = nodes or []
        self.materials = materials or []
        self.properties = properties or []
        self.elements = elements or []
        self.loads = loads or []
        self.constraints = constraints or []
        self.name = name
        
        self.K = None  # Global stiffness matrix
        self.F = None  # Global force vector
        self.q = None  # Global displacement vector

    def assign_global_dof(self):
        """
        Assign global degrees of freedom (DOF) to each node and initialize matrices.
        """
        global_dof = 0
        for node in self.nodes:
            for dof in range(node.dof):
                node.global_dof[dof] = global_dof
                global_dof += 1
        
        self.K = np.zeros((global_dof, global_dof))
        self.F = np.full((global_dof, 1), np.nan)
        self.q = np.full((global_dof, 1), np.nan)

    def assemble_stiffness_matrix(self):
        """
        Assemble the global stiffness matrix by summing element stiffness matrices.
        """
        for element in self.elements:
            dofs = [dof for node in element.nodes for dof in node.global_dof]
            for i, dof1 in enumerate(dofs):
                for j, dof2 in enumerate(dofs):
                    self.K[dof1, dof2] += element.K_global_coord[i, j]

    def assemble_displacements_vector(self):
        """
        Assemble the global displacement vector based on constraints.
        """
        for constraint in self.constraints:
            node = self.nodes[constraint.node]
            dof = node.global_dof[constraint.dof]
            self.q[dof] = constraint.value

    def assemble_force_vector(self):
        """
        Assemble the global force vector based on applied loads.
        """
        self.F[np.isnan(self.q)] = 0
        for load in self.loads:
            node = self.nodes[load.node]
            dof = node.global_dof[load.dof]
            self.F[dof] = load.value

    def solve(self):
        """
        Solve for the unknown displacements using the reduced system of equations.
        """
        dof_red = np.where(np.isnan(self.q))[0]
        F_red = self.F[dof_red]
        K_red = self.K[np.ix_(dof_red, dof_red)]
        q_red = np.linalg.solve(K_red, F_red)
        
        for i, dof in enumerate(dof_red):
            self.q[dof] = q_red[i]
        
        self.F = np.dot(self.K, self.q)

    def calculate_displacements(self):
        """
        Update the displacement for each node based on the global displacement vector.
        """
        for node in self.nodes:
            for i in range(node.dof):
                node.displacement[i] = float(self.q[node.global_dof[i]])
        for element in self.elements:
            element.calculate_deformed()
    
    def calculate_forces(self):
        """
        Update the displacement for each node based on the global displacement vector.
        """
        for node in self.nodes:
            for i in range(node.dof):
                node.force[i] = float(self.F[node.global_dof[i]])

    def plot(self, factor = 1.0):
        plt.figure()
        for element in self.elements:
            plt.plot(
                element.xcurve+factor*element.xdeformed,
                element.ycurve+factor*element.ydeformed
            )
        plt.show()

    '''def get_positions(self):
        """
        Retrieve the original and deformed positions of the nodes in the elements.
        """
        XX, YY, dXX, dYY = [], [], [], []
        for element in self.elements:
            xx, yy, dxx, dyy = [], [], [], []
            for node in element.nodes:
                xx.append(node.position[0])
                yy.append(node.position[1])
                dxx.append(node.displacement[0])
                dyy.append(node.displacement[1])
            XX.append(xx)
            YY.append(yy)
            dXX.append(dxx)
            dYY.append(dyy)
        return XX, YY, dXX, dYY
    
    def plot(self, factor=1.0):
        """
        Plot the undeformed and deformed shapes of the model.
        
        :param factor: Scale factor for the deformed shape.
        """
        plt.figure(figsize=(10, 8))
        XX, YY, dXX, dYY = self.get_positions()
        
        for xx, yy, dxx, dyy in zip(XX, YY, dXX, dYY):
            plt.plot(xx, yy, 'o--', color='gray', label='Undeformed Shape')  # Undeformed shape
            plt.plot([x + factor * dx for x, dx in zip(xx, dxx)], 
                    [y + factor * dy for y, dy in zip(yy, dyy)], 
                    'o-', color='blue', label='Deformed Shape')  # Deformed shape
        
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title('Undeformed and Deformed Shapes')
        plt.axis('equal')  # Ensure aspect ratio is equal to show accurate deformations
        plt.show()'''

    def generate_report(self):
        report = f"Model Report: {self.name}\n"
        report += f"  Number of Nodes       : {len(self.nodes)}\n"
        report += f"  Number of Elements    : {len(self.elements)}\n"
        report += f"  Number of Materials   : {len(self.materials)}\n"
        report += f"  Number of Properties  : {len(self.properties)}\n"
        report += f"  Number of Loads       : {len(self.loads)}\n"
        report += f"  Number of Constraints : {len(self.constraints)}\n"
        report += f"  Global DOF            : {self.K.shape[0] if self.K is not None else 'Not assigned'}\n"

        # Displacements
        report += "\n  Displacements:\n"
        report += "  ----------------------\n"
        for i, node in enumerate(self.nodes):
            disp = node.displacement
            report += f"    Node {i}: X = {disp[0]:.2f}, Y = {disp[1]:.2f}\n"

        # Forces
        # Displacements
        report += "\n  Forces:\n"
        report += "  ----------------------\n"
        for i, node in enumerate(self.nodes):
            force = node.force
            report += f"    Node {i}: X = {force[0]:.2f}, Y = {force[1]:.2f}\n"
        
        print(report)


    def __repr__(self):
        return (f"Model: {self.name}\n"
                f"  * Number of Nodes       : {len(self.nodes)}\n"
                f"  * Number of Elements    : {len(self.elements)}\n"
                f"  * Number of Materials   : {len(self.materials)}\n"
                f"  * Number of Properties  : {len(self.properties)}\n"
                f"  * Number of Loads       : {len(self.loads)}\n"
                f"  * Number of Constraints : {len(self.constraints)}\n"
                f"  * Global DOF            : {self.K.shape[0] if self.K is not None else 'Not assigned'}\n")

