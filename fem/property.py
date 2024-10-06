import numpy as np
from fem.material import Material

class Property:
    property_count = 0

    def __init__(self, name: str):
        """
        Initialize a Property.

        :param name: Name of the property.
        """
        self.id = Property.property_count
        Property.property_count += 1
        self.name = name

    def __repr__(self) -> str:
        return (f"Property:\n ID = {self.id}\n Name = {self.name}\n"
                f"Material = {self.material.material_id}\n")


class Rod(Property):
    def __init__(self, name: str, material: Material, area: float):
        """
        Initialize a Rod.

        :param name: Name of the rod.
        :param material: Material object associated with the rod.
        :param area: Cross-sectional area of the rod.
        """
        super().__init__(name)
        self.material = material
        self.area = area

    def phi(self, xi):
        """
        Shape function for the rod element.
        
        :param xi: Local coordinate along the length of the rod (typically from 0 to 1).
        :return: Shape function evaluated at xi.
        """
        return np.array([[1 - xi, xi]])


class Beam2D(Property):
    def __init__(self, name: str, material: Material, area: float, Izz: float):
        """
        Initialize a 2D Beam.

        :param name: Name of the beam.
        :param material: Material object associated with the beam.
        :param area: Cross-sectional area of the beam.
        :param Izz: Second moment of area (moment of inertia) about the z-axis.
        """
        super().__init__(name)
        self.material = material
        self.area = area
        self.Izz = Izz

    def __repr__(self) -> str:
        return (f"Beam2D:\n ID = {self.id}\n Name = {self.name}\n"
                f"Material = {self.material.material_id}\n Area = {self.area}\n Izz = {self.Izz}")

class Membrane(Property):
    def __init__(self, name: str, material: Material, t: float, plane_stress=True):
        """
        Initialize a Membrane.

        :param name: Name of the membrane.
        :param material: Material object associated with the membrane.
        :param t: Thickness of the membrane.
        :param plane_stress: Boolean indicating if the membrane is under plane stress conditions (default is True).
        """
        super().__init__(name)  # Use super() to call the parent constructor
        self.material = material
        self.thickness = t  # Renamed 't' to 'thickness' for clarity
        self.plane_stress = plane_stress

    def __repr__(self) -> str:
        """
        String representation of the Membrane.
        """
        stress_condition = "Plane Stress" if self.plane_stress else "Plane Strain"
        return (f"Membrane:\n ID = {self.id}\n Name = {self.name}\n"
                f"Material = {self.material.material_id}\n Thickness = {self.thickness}\n"
                f"Condition = {stress_condition}")

