class Property:
    def __init__(self, property_id, material, area):
        """
        Initialize a Property.
        
        :param material: Material object.
        :param area: Cross section area.

        """
        self.property_id = property_id
        self.material = material
        self.area = area

    def __repr__(self):
        return f"Property(Material={self.material.material_id}, area={self.area})"