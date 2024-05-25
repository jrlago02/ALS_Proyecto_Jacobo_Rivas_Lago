import uuid

class Plato:
    def __init__(self, nombre, descripcion, precio):
        self._id = str(uuid.uuid4())  
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.calificaciones = []

    @property
    def nota_media(self):
        if not self.calificaciones:
            return 0
        return round(sum(self.calificaciones) / len(self.calificaciones), 1)

    def agregar_calificacion(self, nota):
        self.calificaciones.append(nota)

    def __repr__(self):
        return f'<Plato {self.nombre}>'
