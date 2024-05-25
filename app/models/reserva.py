import datetime
import sirope
import uuid

class Reserva:
    def __init__(self, user_id, numero_mesa, num_personas, fecha_hora):
        self._id = str(uuid.uuid4()) 
        self.user_id = user_id
        self.numero_mesa = numero_mesa
        self.num_personas = num_personas
        self.fecha_hora = datetime.datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M') if isinstance(fecha_hora, str) else fecha_hora

    def __repr__(self):
        return f'<Reserva {self._id}>'
