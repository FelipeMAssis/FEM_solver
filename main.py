import numpy as np
from fem.node import Node
from fem.element import Element
from fem.material import Material
from fem.property import Rod
from fem.boundary_condition import NodalConstraint, NodalLoad
from fem.model import Model

def get_input(prompt, type_=str, default=None, valid_values=None):
    while True:
        try:
            value = input(prompt)
            if not value and default is not None:
                return default
            value = type_(value)
            if valid_values and value not in valid_values:
                print(f"Invalid input. Expected one of {valid_values}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please try again.")

def get_nodes():
    num_nodes = get_input("Enter the number of nodes: ", int)
    nodes = []
    for i in range(num_nodes):
        x = get_input(f"Enter x position for node {i} (e.g., 100.0): ", float)
        y = get_input(f"Enter y position for node {i} (e.g., 200.0): ", float)
        nodes.append(Node(i, [x, y]))
    return nodes

def get_material():
    material_id = get_input("Enter material ID: ", int)
    youngs_modulus = get_input("Enter Young's modulus (e.g., 200000): ", float)
    return Material(material_id, youngs_modulus)

def get_property(material):
    property_id = get_input("Enter property ID: ", int)
    area = get_input("Enter cross-sectional area (e.g., 10.0): ", float)
    return Rod(property_id, material, area)

def get_elements(nodes, rod_property):
    num_elements = get_input("Enter the number of elements: ", int)
    elements = []
    for i in range(num_elements):
        node_ids = list(map(int, get_input(f"Enter node IDs for element {i} (space-separated): ").split()))
        if len(node_ids) < 2:
            print("An element must connect at least two nodes.")
            continue
        elements.append(Element(i, [nodes[id_] for id_ in node_ids], property=rod_property))
    return elements

def get_constraints():
    num_constraints = get_input("Enter the number of constraints: ", int)
    constraints = []
    for _ in range(num_constraints):
        node_id = get_input("Enter node ID for constraint: ", int)
        dof = get_input("Enter DOF for constraint: ", int)
        value = get_input("Enter value for constraint: ", float)
        constraints.append(NodalConstraint(node_id, dof, value))
    return constraints

def get_loads():
    num_loads = get_input("Enter the number of loads: ", int)
    loads = []
    for _ in range(num_loads):
        node_id = get_input("Enter node ID for load: ", int)
        dof = get_input("Enter DOF for load: ", int)
        value = get_input("Enter value for load: ", float)
        loads.append(NodalLoad(node_id, dof, value))
    return loads

def main():
    print("Welcome to the FEM Model Setup.\n")
    
    # Get input from user
    nodes = get_nodes()
    material = get_material()
    rod_property = get_property(material)
    elements = get_elements(nodes, rod_property)
    constraints = get_constraints()
    loads = get_loads()

    # Create and run the model
    model = Model(
        nodes=nodes,
        materials=[material],
        properties=[rod_property],
        elements=elements,
        loads=loads,
        constraints=constraints
    )

    model.assign_global_dof()
    model.assemble_stiffness_matrix()
    model.assemble_displacements_vector()
    model.assemble_force_vector()
    model.solve()
    model.calculate_displacements()

    # Print results
    print("\nDisplacements:\n", model.q)
    model.plot(factor=1)

if __name__ == "__main__":
    main()

