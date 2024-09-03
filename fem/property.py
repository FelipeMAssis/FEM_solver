import numpy as np
from fem.material import Material

class Rod:
    def __init__(self, property_id: int, name: str, material: Material, area: float):
        """
        Initialize a Rod.
        
        :param property_id: Unique identifier for the rod.
        :param name: Name of the rod.
        :param material: Material object associated with the rod.
        :param area: Cross-sectional area of the rod.
        """
        self.property_id = property_id
        self.name = name
        self.material = material
        self.area = area

    def phi(self, xi):
        return np.array([[1-xi, xi]])

    def __repr__(self) -> str:
        return (f"Rod: {self.name}(id={self.property_id}, "
                f"material={self.material.material_id}, area={self.area})")


class Bar2D:
    def __init__(self, property_id: int, name: str, material: Material, area: float, Izz: float):
        """
        Initialize a 2D Bar.
        
        :param property_id: Unique identifier for the rod.
        :param name: Name of the rod.
        :param material: Material object associated with the rod.
        :param area: Cross-sectional area of the rod.
        :param Iyy: 
        """
        self.property_id = property_id
        self.name = name
        self.material = material
        self.area = area
        self.Izz = Izz

    def __repr__(self) -> str:
        return (f"Bar: {self.name}(id={self.property_id}, "
                f"material={self.material.material_id}, area={self.area}, Izz={self.Izz})")

