import uuid

class Mesa:
    def __init__(self, numero, capacidad, disponible=True, top=0, left=0):
        self._id = str(uuid.uuid4())
        self.numero = numero
        self.capacidad = capacidad
        self.disponible = disponible
        self.top = top
        self.left = left

    def __repr__(self):
        return f'<Mesa {self.numero}>'
