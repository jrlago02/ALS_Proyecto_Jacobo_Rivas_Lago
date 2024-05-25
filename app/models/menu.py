import uuid

class Menu:
    def __init__(self, nombre, descripcion, platos_ids):
        self._id = str(uuid.uuid4())
        self.nombre = nombre
        self.descripcion = descripcion
        self.platos_ids = platos_ids  # Almacenar los IDs de los platos

    def __repr__(self):
        return f'<Menu {self.nombre}>'
