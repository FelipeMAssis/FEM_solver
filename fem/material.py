class Material:
    material_count = 0

    def __init__(self, name: str, youngs_modulus: float, poissons_ratio=None):
        """
        Initialize a Material.
        
        :param name: Name of the material.
        :param youngs_modulus: Young's modulus of the material.
        """
        self.material_id = Material.material_count
        Material.material_count += 1
        self.name = name
        self.youngs_modulus = youngs_modulus
        self.poissons_ratio = poissons_ratio

    def __repr__(self) -> str:
        return f"Material:\n ID = {self.material_id}\n Name = {self.name}"

