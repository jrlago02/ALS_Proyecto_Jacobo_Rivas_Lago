# app/models/propuesta_plato.py
import sirope
import uuid

class PropuestaPlato:
    def __init__(self, user_id, titulo, descripcion, precio_max, nota):
        self._id = str(uuid.uuid4()) 
        self.user_id = user_id
        self.titulo = titulo
        self.descripcion = descripcion
        self.precio_max = precio_max
        self.nota = nota

    def __repr__(self):
        return f'<PropuestaPlato {self.titulo}>'
