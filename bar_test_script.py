import numpy as np
from fem.node import Node
from fem.element import BarElement
from fem.material import Material
from fem.property import Bar2D
from fem.boundary_condition import NodalConstraint, NodalLoad
from fem.model import Model

def run_test_case():
    # Define nodes
    nodes = [
        Node(0, [0, 0], 3),
        Node(1, [0, 1000], 3),
        Node(2, [1000, 0], 3)
    ]

    # Define material
    aluminum = Material(0, "Alluminum", 80000)

    # Define property
    bar = Bar2D(0, "MyRod", aluminum, 100, 10000/12)

    # Define elements
    elements = [
        BarElement(0, [nodes[0], nodes[1]], property=bar),
        BarElement(1, [nodes[1], nodes[2]], property=bar),
    ]

    # Define constraints
    constraints = [
        NodalConstraint(0, 0, 0),
        NodalConstraint(0, 1, 0),
        NodalConstraint(0, 2, 0),
        NodalConstraint(2, 0, 0),
        NodalConstraint(2, 1, 0),
        NodalConstraint(2, 2, 0)
    ]

    # Define loads
    loads = [
        NodalLoad(1, 0, -10000),
    ]

    # Create model
    model = Model(
        nodes=nodes,
        materials=[aluminum],
        properties=[bar],
        elements=elements,
        loads=loads,
        constraints=constraints
    )

    # Run analysis
    model.assign_global_dof()
    model.assemble_stiffness_matrix()
    model.assemble_displacements_vector()
    model.assemble_force_vector()
    model.solve()
    model.calculate_displacements()
    model.calculate_forces()
    # Print results
    model.generate_report()
    model.plot(factor=1)

if __name__ == "__main__":
    run_test_case()