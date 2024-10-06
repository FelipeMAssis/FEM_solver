import numpy as np
from fem.material import Material

property_count = 0

class Property:
    def __init__(self, name: str):
        global property_count
        self.id = property_count
        property_count = property_count + 1
        self.name = name

    def __repr__(self) -> str:
        return (f"Rod:\n ID = {self.id}\n Name = {self.name}\n"
                f" Material = {self.material.material_id}\n")

class Rod(Property):
    def __init__(self, name: str, material: Material, area: float):
        """
        Initialize a Rod.
        
        :param property_id: Unique identifier for the rod.
        :param name: Name of the rod.
        :param material: Material object associated with the rod.
        :param area: Cross-sectional area of the rod.
        """
        Property.__init__(self, name)
        self.material = material
        self.area = area

    def phi(self, xi):
        return np.array([[1-xi, xi]])


class Beam2D(Property):
    def __init__(self, name: str, material: Material, area: float, Izz: float):
        """
        Initialize a 2D Bar.
        
        :param property_id: Unique identifier for the rod.
        :param name: Name of the rod.
        :param material: Material object associated with the rod.
        :param area: Cross-sectional area of the rod.
        :param Iyy: 
        """
        Property.__init__(self, name)
        self.name = name
        self.material = material
        self.area = area
        self.Izz = Izz

class 

