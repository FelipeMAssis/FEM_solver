import numpy as np
from fem.node import Node
from fem.element import Element
from fem.material import Material
from fem.property import Rod
from fem.boundary_condition import NodalConstraint, NodalLoad
from fem.model import Model

def run_test_case():
    # Define nodes
    nodes = [
        Node(0, [0, 0]),
        Node(1, [1200, 300]),
        Node(2, [2400, 0]),
        Node(3, [1200, 800])
    ]

    # Define material
    aluminum = Material(0, 80000)

    # Define property
    rod = Rod(0, aluminum, 100)

    # Define elements
    elements = [
        Element(0, [nodes[0], nodes[1]], property=rod),
        Element(1, [nodes[1], nodes[2]], property=rod),
        Element(2, [nodes[0], nodes[3]], property=rod),
        Element(3, [nodes[1], nodes[3]], property=rod),
        Element(4, [nodes[2], nodes[3]], property=rod)
    ]

    # Define constraints
    constraints = [
        NodalConstraint(0, 0, 0),
        NodalConstraint(0, 1, 0),
        NodalConstraint(2, 1, 0)
    ]

    # Define loads
    loads = [
        NodalLoad(3, 0, -30000),
        NodalLoad(3, 1, 20000),
    ]

    # Create model
    model = Model(
        nodes=nodes,
        materials=[aluminum],
        properties=[rod],
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

    # Print results
    print("Displacements:\n", model.q)
    model.plot(factor=1)

if __name__ == "__main__":
    run_test_case()
