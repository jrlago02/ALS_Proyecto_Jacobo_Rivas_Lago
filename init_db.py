import sirope
from app.models.plato import Plato
from app.models.menu import Menu
from app.models.mesa import Mesa
from app.models.reserva import Reserva
from app.models.user import User
from app.models.calificacion import Calificacion
from werkzeug.security import generate_password_hash
import redis
import uuid
import random

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Limpiar toda la base de datos de Redis por si queremos hacer prueba desde 0
redis_client.flushdb()

s = sirope.Sirope()

platos = [
    Plato(nombre="Ensalada César", descripcion="Ensalada con salsa César y pollo", precio=8.50),
    Plato(nombre="Sopa de Tomate", descripcion="Sopa de tomate cremosa con crutones", precio=6.00),
    Plato(nombre="Gazpacho", descripcion="Sopa fría de tomate y pepino, especialidad de verano", precio=5.50),
    Plato(nombre="Bruschetta", descripcion="Pan tostado con tomate, ajo y albahaca", precio=7.00),
    Plato(nombre="Calamares a la Romana", descripcion="Calamares rebozados servidos con alioli", precio=9.00),
    Plato(nombre="Croquetas de Jamón", descripcion="Croquetas crujientes de jamón ibérico", precio=8.00),
    Plato(nombre="Empanadas", descripcion="Empanadas rellenas de carne, especias y aceitunas", precio=7.50),
    Plato(nombre="Tortilla Española", descripcion="Tortilla de patatas tradicional", precio=6.50),
    Plato(nombre="Paella de Mariscos", descripcion="Paella con una mezcla de mariscos frescos", precio=15.00),
    Plato(nombre="Solomillo al Oporto", descripcion="Solomillo de ternera con salsa de vino Oporto", precio=18.50),
    Plato(nombre="Pollo al Curry", descripcion="Pollo cocido en una rica salsa de curry", precio=14.00),
    Plato(nombre="Bacalao a la Vizcaína", descripcion="Bacalao en salsa de tomate y pimientos", precio=16.00),
    Plato(nombre="Lasaña", descripcion="Lasaña de carne y queso con salsa de tomate", precio=12.00),
    Plato(nombre="Raviolis de Espinacas", descripcion="Raviolis rellenos de espinacas y ricotta", precio=13.00),
    Plato(nombre="Filete de Salmon", descripcion="Filete de salmón a la parrilla con hierbas", precio=17.00),
    Plato(nombre="Costillas BBQ", descripcion="Costillas de cerdo con salsa barbacoa", precio=19.00)
]

plato_ids = []
for plato in platos:
    s.save(plato)
    plato_ids.append(plato._id)

menus = [
    Menu(nombre="Menú del Día", descripcion="Platos frescos cada día", platos_ids=[plato_ids[0], plato_ids[8], plato_ids[1]]),
    Menu(nombre="Menú Vegetariano", descripcion="Deliciosa variedad de platos vegetarianos", platos_ids=[plato_ids[2], plato_ids[7], plato_ids[13]]),
    Menu(nombre="Menú Mar y Tierra", descripcion="Combinación de mar y carne", platos_ids=[plato_ids[4], plato_ids[10], plato_ids[14]]),
    Menu(nombre="Menú Italiano", descripcion="Sabores clásicos de Italia", platos_ids=[plato_ids[3], plato_ids[11], plato_ids[13]]),
    Menu(nombre="Menú Español", descripcion="Platos tradicionales", platos_ids=[plato_ids[7], plato_ids[9], plato_ids[15]]),
    Menu(nombre="Menú Especial", descripcion="Selección especial del chef", platos_ids=[plato_ids[1], plato_ids[5], plato_ids[13]])
]

for menu in menus:
    s.save(menu)

mesas = [
    Mesa(numero=1, capacidad=2, disponible=True, top=50, left=100),
    Mesa(numero=2, capacidad=4, disponible=True, top=50, left=200),
    Mesa(numero=3, capacidad=6, disponible=True, top=150, left=100),
    Mesa(numero=4, capacidad=8, disponible=True, top=150, left=300),
    Mesa(numero=5, capacidad=10, disponible=True, top=250, left=100)
]

# Guardar mesas en la base de datos
for mesa in mesas:
    s.save(mesa)

for plato in platos:
    calificaciones = []
    for _ in range(5):
        nota = round(random.uniform(0, 5),1) 
        calificacion = Calificacion(user_id=str(uuid.uuid4()), plato_id=plato._id, nota=nota)
        s.save(calificacion)
        calificaciones.append(nota)
    plato.calificaciones = calificaciones
    s.save(plato)

password_hash = generate_password_hash("password123")
user = User(username="testuser", email="testuser@example.com", password=password_hash)
s.save(user)

reserva_antigua = Reserva(user_id=user.get_id(), numero_mesa=1, num_personas=2, fecha_hora="2023-12-20 12:00")
s.save(reserva_antigua)

print("Base de datos inicializada con éxito.")
