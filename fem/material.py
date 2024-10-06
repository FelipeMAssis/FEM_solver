material_count=0

class Material:
    def __init__(self, name: str, youngs_modulus: float):
        """
        Initialize a Material.
        
        :param material_id: Unique identifier for the material.
        :param name: Name of the material.
        :param youngs_modulus: Young's modulus of the material.
        """
        global material_count
        self.material_id = material_count
        material_count = material_count + 1
        self.name = name
        self.youngs_modulus = youngs_modulus

    def __repr__(self) -> str:
        return f"Material:\n ID = {self.material_id}\n Name = {self.name}\n E = {self.youngs_modulus}"
