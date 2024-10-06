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
            plt.plot(xundef, yundef, 'o--', color='gray', label='Undeformed Shape')

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

        scalex = max([abs(n.position[0]+factor*n.displacement[0]) for n in self.nodes])
        scaley = max([abs(n.position[1]+factor*n.displacement[1]) for n in self.nodes])
        scale = max([scalex,scaley])

        scalef = max([abs(l.value) for l in self.loads])

        if show_constraints:
            for constraint in self.constraints:
                x, y = [p+factor*d for p, d in zip(self.nodes[constraint.node].position, self.nodes[constraint.node].displacement)]
                plt.arrow(x-0.1*(1-constraint.dof), y-0.1*constraint.dof, 0.1*(1-constraint.dof), 0.1*constraint.dof, head_length=0.04*scale, head_width=0.02*scale, length_includes_head=True, color='cyan')

        if show_force:
            for load in self.loads:
                x, y = [p+factor*d for p, d in zip(self.nodes[load.node].position, self.nodes[load.node].displacement)]
                plt.arrow(x, y, load.value*(1-load.dof)*0.5*scale/scalef, load.value*load.dof*0.5*scale/scalef, head_length=0.04*scale, head_width=0.02*scale, length_includes_head=True, color='green')

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(f'Undeformed and Deformed Shapes (Scale factor = {factor:.1f}, Contour = {contour}, Text = {text})')
        plt.axis('equal')  # Ensure aspect ratio is equal to show accurate deformations
        plt.legend(['Undeformed Shape', 'Deformed Shape'])
        plt.show()

    def plot2DArea(self, factor=0, show_constraints=False, show_force=False):
        plt.figure(figsize=(10, 8))

        for element in self.elements:
            xundef = np.array([element.nodes[0].position[0], element.nodes[1].position[0], element.nodes[2].position[0], element.nodes[0].position[0]])
            yundef = np.array([element.nodes[0].position[1], element.nodes[1].position[1], element.nodes[2].position[1], element.nodes[0].position[1]])
            xdef = xundef+factor*np.array([element.nodes[0].displacement[0], element.nodes[1].displacement[0], element.nodes[2].displacement[0], element.nodes[0].displacement[0]])
            ydef = yundef+factor*np.array([element.nodes[0].displacement[1], element.nodes[1].displacement[1], element.nodes[2].displacement[1], element.nodes[0].displacement[1]])
            plt.plot(xundef, yundef, 'o--', color='gray', label='Undeformed Shape')
            plt.fill(xundef, yundef, color='gray', alpha=0.2, label='_nolegend_')
            plt.plot(xdef, ydef, 'o-', markerfacecolor='k', markeredgecolor='k', color='k', label='Deformed Shape')
            plt.fill(xdef, ydef, color='k', alpha=0.2,label='_nolegend_')

        scalex = max([abs(n.position[0]+factor*n.displacement[0]) for n in self.nodes])
        scaley = max([abs(n.position[1]+factor*n.displacement[1]) for n in self.nodes])
        scale = max(scalex,scaley)

        scalef = max([abs(l.value) for l in self.loads])

        if show_constraints:
            for constraint in self.constraints:
                x, y = [p+factor*d for p, d in zip(self.nodes[constraint.node].position, self.nodes[constraint.node].displacement)]
                plt.arrow(x-0.1*(1-constraint.dof), y-0.1*constraint.dof, 0.1*(1-constraint.dof), 0.1*constraint.dof, head_length=0.04*scale, head_width=0.02*scale, length_includes_head=True, color='cyan')

        if show_force:
            for load in self.loads:
                x, y = [p+factor*d for p, d in zip(self.nodes[load.node].position, self.nodes[load.node].displacement)]
                plt.arrow(x, y, load.value*(1-load.dof)*0.5*scale/scalef, load.value*load.dof*0.5*scale/scalef, head_length=0.04*scale, head_width=0.02*scale, length_includes_head=True, color='green')

        plt.xlabel('X Coordinate')
        plt.ylabel('Y Coordinate')
        plt.title(f'Undeformed and Deformed Shapes (Scale factor = {factor:.1f})')
        plt.axis('equal')  # Ensure aspect ratio is equal to show accurate deformations
        plt.legend(['Undeformed Shape', 'Deformed Shape'])
        plt.show()