class Material:
    def __init__(self, material_id, youngs_modulus):
        """
        Initialize a Material.
        
        :param youngs_modulus: Young's modulus of the material.
        """
        self.material_id = material_id
        self.youngs_modulus = youngs_modulus

    def __repr__(self):
        return f"Material(E={self.youngs_modulus})"
