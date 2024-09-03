class Material:
    def __init__(self, material_id: int, name: str, youngs_modulus: float):
        """
        Initialize a Material.
        
        :param material_id: Unique identifier for the material.
        :param name: Name of the material.
        :param youngs_modulus: Young's modulus of the material.
        """
        self.material_id = material_id
        self.name = name
        self.youngs_modulus = youngs_modulus

    def __repr__(self) -> str:
        return f"Material: {self.name}(Material ID={self.material_id}, E={self.youngs_modulus})"
