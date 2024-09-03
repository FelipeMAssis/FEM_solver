import numpy as np
from fem.node import Node
from fem.element import Element
from fem.material import Material
from fem.property import Property
from fem.load import NodalLoad
from fem.constraint import NodalConstraint
from fem.model import Model
from fem.analysis import Analysis

nodes = [
    Node(0, [0,0]),
    Node(1, [1200,300]),
    Node(2, [2400, 0]),
    Node(3, [1200, 800])
]

alluminum = Material(0, 80000)

rod = Property(0, alluminum, 100)

elements = [
    Element(0,[nodes[0], nodes[1]], property=rod),
    Element(1,[nodes[1], nodes[2]], property=rod),
    Element(2,[nodes[0], nodes[3]], property=rod),
    Element(3,[nodes[1], nodes[3]], property=rod),
    Element(4,[nodes[2], nodes[3]], property=rod)
]

constraints = [
    NodalConstraint(0, [1,2], [0,0]),
    NodalConstraint(2, 1, 0)
    
]

loads = [
    NodalLoad(3,[1,2],[-30,20])
]

model = Model(
    nodes=nodes,
    materials=[alluminum],
    properties=[rod],
    elements=elements,
    loads=loads,
    constraints=constraints
)

analysis = Analysis(model)


for element in elements:
    print(element)