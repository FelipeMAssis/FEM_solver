class Rod:
    def __init__(self, property_id, material, area):
        """
        Initialize a Property.
        
        :param property_id: Unique identifier for the property.
        :param material: Material object associated with the property.
        :param area: Cross-sectional area of the element.
        """
        self.property_id = property_id
        self.material = material
        self.area = area

    def __repr__(self):
        return f"Rod(id={self.property_id}, material={self.material.material_id}, area={self.area})"
