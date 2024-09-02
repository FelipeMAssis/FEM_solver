import numpy as np
from fem.nodes import Node
from fem.elements import Element
from fem.material import Material
from fem.properties import Property

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
    Element(4,[nodes[3], nodes[2]], property=rod)
]



