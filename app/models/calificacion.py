import uuid

class Calificacion:
    def __init__(self, user_id, plato_id, nota):
        self._id = str(uuid.uuid4())  # Genera un UUID para cada calificación
        self.user_id = user_id
        self.plato_id = plato_id
        self.nota = nota

    def __repr__(self):
        return f'<Calificacion {self.user_id} {self.plato_id}>'
