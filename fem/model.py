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
    
    def calculate_forces(self):
        """
        Update the displacement for each node based on the global displacement vector.
        """
        for node in self.nodes:
            for i in range(node.dof):
                node.force[i] = float(self.F[node.global_dof[i]])
    
    def caclulate_element_results(self):
        for element in self.elements:
            element.calculate_local_results()

    
    def plot(self, factor=0):
        """
        Plot the undeformed and deformed shapes of the model.
        
        :param factor: Scale factor for the deformed shape.
        """
        plt.figure(figsize=(10, 8))
        for element in self.elements:
            xundef = np.array([element.nodes[0].position[0], element.nodes[1].position[0]])
            yundef = np.array([element.nodes[0].position[1], element.nodes[1].position[1]])
            xdef = xundef+factor*np.array([element.nodes[0].displacement[0], element.nodes[1].displacement[0]])
            ydef = yundef+factor*np.array([element.nodes[0].displacement[1], element.nodes[1].displacement[1]])
            plt.plot(xundef, yundef, 'o--', color='gray', label='Undeformed Shape')
            plt.plot(xdef, ydef, 'o-', color='blue', label='Deformed Shape')
        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(f'Undeformed and Deformed Shapes (Scale factor = {factor:.1f})')
        plt.axis('equal')  # Ensure aspect ratio is equal to show accurate deformations
        plt.legend(['Undeformed Shape', 'Deformed Shape'])
        plt.show()


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
            report += f"    Node {i}:"
            for d in disp:
                report+=f"\t{d:.4f}"
            report+="\n"

        # Forces
        # Displacements
        report += "\n  Forces:\n"
        report += "  ----------------------\n"
        for i, node in enumerate(self.nodes):
            force = node.force
            report += f"    Node {i}:"
            for f in force:
                report+=f"\t{f:.4f}"
            report+="\n"
        
        print(report)
    

    def element_report(self):
        # Deformations
        report = "\n  Deformations:\n"
        report += "  ----------------------\n"
        for i, element in enumerate(self.elements):
            report += f"    Element {i}:\t{element.deformation:.4f}\n"
        
        report += "\n  Forces:\n"
        report += "  ----------------------\n"
        for i, element in enumerate(self.elements):
            report += f"    Element {i}:\t{element.force:.4f}\n"
        
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

