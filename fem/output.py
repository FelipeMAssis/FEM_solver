import numpy as np
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle

cmap = plt.get_cmap('jet')

class Output:
    def __init__(self, model):
        self.nodes = model.nodes
        self.elements = model.elements
        self.constraints = model.constraints
        self.loads = model.loads
        self.q = model.q
        self.F = model.F

    def compute_nodal_results(self):
        for node in self.nodes:
            for i in range(node.dof):
                node.displacement[i] = float(self.q[node.global_dof[i]])
        for node in self.nodes:
            for i in range(node.dof):
                node.force[i] = float(self.F[node.global_dof[i]])
    
    def compute_element_results(self):
        for elem in self.elements:
            elem.calculate_local_results()


    def plot2DBars(self, factor=0, contour=None, text=None, show_constraints=False, show_force=False):
        """
        Plot the undeformed and deformed shapes of the model.
        
        :param factor: Scale factor for the deformed shape.
        """
        plt.figure(figsize=(10, 8))

        if contour == 'Force':
            values = [elem.force for elem in self.elements]
            max_value = max(values)
            min_value = min(values)
        elif contour == 'Deformation':
            values = [elem.deformation for elem in self.elements]
            max_value = max(values)
            min_value = min(values)

        for element in self.elements:
            xundef = np.array([element.nodes[0].position[0], element.nodes[1].position[0]])
            yundef = np.array([element.nodes[0].position[1], element.nodes[1].position[1]])
            xdef = xundef+factor*np.array([element.nodes[0].displacement[0], element.nodes[1].displacement[0]])
            ydef = yundef+factor*np.array([element.nodes[0].displacement[1], element.nodes[1].displacement[1]])
            plt.plot(xundef, yundef, '--', color='gray', label='Undeformed Shape')

            if text == 'Deformation':
                plt.text(np.mean(xdef),np.mean(ydef),"{:.2f}".format(element.deformation))
            elif text == 'Force':
                plt.text(np.mean(xdef),np.mean(ydef),"{:.0f}".format(element.force))

            if contour == 'Deformation':
                color = cmap(0.1+0.8*(element.deformation-min_value)/(max_value-min_value))
                
            elif contour == 'Force':
                if text:
                    plt.text(np.mean(xdef),np.mean(ydef),"{:.0f}".format(element.force))
                color = cmap(0.1+0.8*(element.force-min_value)/(max_value-min_value))
                
            else:
                color = 'k'
            plt.plot(xdef, ydef, 'o-', markerfacecolor='k', markeredgecolor='k', color=color, label='Deformed Shape')

        if show_constraints:
            for constraint in self.constraints:
                x, y = self.nodes[constraint.node].position
                plt.arrow(x-0.1*(1-constraint.dof), y-0.1*constraint.dof, 0.1*(1-constraint.dof), 0.1*constraint.dof, head_length=100, head_width=50, length_includes_head=True, color='cyan')

        if show_force:
            for load in self.loads:
                x, y = self.nodes[load.node].position
                plt.arrow(x, y, load.value*(1-load.dof)/10, load.value*load.dof/10, head_length=100, head_width=50, length_includes_head=True, color='green')

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(f'Undeformed and Deformed Shapes (Scale factor = {factor:.1f}, Contour = {contour}, Text = {text})')
        plt.axis('equal')  # Ensure aspect ratio is equal to show accurate deformations
        plt.legend(['Undeformed Shape', 'Deformed Shape'])
        plt.show()

    '''
    def caclulate_element_results(self):
        for element in self.elements:
            element.calculate_local_results()


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
                f"  * Number of Constraints : {len(self.constraints)}\n")
    '''