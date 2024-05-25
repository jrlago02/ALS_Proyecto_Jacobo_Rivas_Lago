from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash, jsonify
from flask_login import login_required, current_user
from ..models.plato import Plato
from ..models.calificacion import Calificacion
from ..models.reserva import Reserva  # Asegúrate de importar la clase Reserva
import sirope
from datetime import datetime

calificacion_bp = Blueprint('calificacion', __name__)

@calificacion_bp.route('/calificacion', methods=['GET', 'POST'])
@login_required
def index():
    s = current_app.config['sirope']
    platos = list(s.load_all(Plato))

    reservas_antiguas = [r for r in s.load_all(Reserva) if r.user_id == current_user.get_id() and r.fecha_hora < datetime.now()]

    if request.method == 'POST':
        if not reservas_antiguas:
            flash('Debes haber tenido una reserva en el pasado para poder calificar.')
            return redirect(url_for('calificacion.html'))

        plato_id = request.form.get('plato_id')
        nota = round(float(request.form.get('nota')), 1) 
        calificacion = Calificacion(user_id=current_user.get_id(), plato_id=plato_id, nota=nota)
        s.save(calificacion)
        
        plato = next((p for p in s.load_all(Plato) if p._id == plato_id), None)
        if plato:
            plato.agregar_calificacion(nota)
            s.save(plato)
        
        return redirect(url_for('calificacion.index', plato_id=plato_id))
    
    plato_id = request.args.get('plato_id')
    calificaciones = []
    nota_media = None
    plato_seleccionado = None
    
    if plato_id:
        plato_seleccionado = next((p for p in platos if p._id == plato_id), None)
        if plato_seleccionado:
            todas_calificaciones = [c for c in s.load_all(Calificacion) if c.plato_id == plato_id]
            calificaciones = todas_calificaciones[-5:]  
            nota_media = round(plato_seleccionado.nota_media, 1) 

    return render_template('calificacion.html', platos=platos, calificaciones=calificaciones, nota_media=nota_media, plato_seleccionado=plato_seleccionado)

@calificacion_bp.route('/calificacion/create', methods=['POST'])
@login_required
def create():
    s = current_app.config['sirope']
    reservas_antiguas = [r for r in s.load_all(Reserva) if r.user_id == current_user.get_id() and r.fecha_hora < datetime.now()]

    if not reservas_antiguas:
        flash('Debes haber tenido una reserva en el pasado para poder calificar.')
        return redirect(url_for('calificacion.index'))

    plato_id = request.form.get('plato_id')
    nota = round(float(request.form.get('nota')), 1)  # Formatear nota a un decimal
    calificacion = Calificacion(user_id=current_user.get_id(), plato_id=plato_id, nota=nota)
    s.save(calificacion)
    
    plato = next((p for p in s.load_all(Plato) if p._id == plato_id), None)
    if plato:
        plato.agregar_calificacion(nota)
        s.save(plato)
        flash('Calificación guardada correctamente.')

    
    return redirect(url_for('calificacion.index', plato_id=plato_id))
