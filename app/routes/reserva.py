from flask import Blueprint, render_template, request, redirect, url_for, jsonify, current_app, flash
from flask_login import login_required, current_user
from ..models.mesa import Mesa
from ..models.reserva import Reserva
from datetime import datetime, timedelta

reserva_bp = Blueprint('reserva', __name__)

def convert_to_datetime(fecha_hora):
    if isinstance(fecha_hora, str):
        return datetime.strptime(fecha_hora, '%Y-%m-%d %H:%M')
    return fecha_hora

@reserva_bp.route('/reserva')
@login_required
def index():
    s = current_app.config['sirope']
    mesas = list(s.load_all(Mesa))
    return render_template('reserva.html', mesas=mesas)

@reserva_bp.route('/reserva/create', methods=['POST'])
@login_required
def create():
    s = current_app.config['sirope']
    num_personas = int(request.form['num_personas'])
    fecha = request.form['fecha']
    hora = request.form['hora']
    fecha_hora = datetime.strptime(f"{fecha} {hora}", '%Y-%m-%d %H:%M')
    fecha_fin_reserva = fecha_hora + timedelta(hours=2)

    if fecha_hora.hour < 12 or fecha_hora.hour >= 22:
        flash('Las reservas solo pueden hacerse entre las 12:00 y las 22:00.')
        return redirect(url_for('reserva.index'))

    mesas = list(s.load_all(Mesa))
    mesas_disponibles = [mesa for mesa in mesas if mesa.capacidad >= num_personas and mesa.capacidad <= num_personas * 2]

    for mesa in mesas_disponibles:
        reservas = list(s.load_all(Reserva))
        reservas_mesa = [reserva for reserva in reservas if reserva.numero_mesa == mesa.numero and reserva.fecha_hora.date() == fecha_hora.date()]
        disponible = True

        for reserva in reservas_mesa:
            reserva_fin = reserva.fecha_hora + timedelta(hours=2)
            if not (fecha_hora >= reserva_fin or fecha_fin_reserva <= reserva.fecha_hora):
                disponible = False
                break
            reserva_fin2 = reserva.fecha_hora - timedelta(hours=2)
            if not (fecha_hora <= reserva_fin2 or fecha_fin_reserva <= reserva.fecha_hora):
                disponible = False
                break
        
        if disponible:
            nueva_reserva = Reserva(user_id=current_user.get_id(), numero_mesa=mesa.numero, num_personas=num_personas, fecha_hora=fecha_hora)
            s.save(nueva_reserva)
            flash('Reserva realizada correctamente.')
            return redirect(url_for('reserva.index'))

    flash('No hay mesas disponibles en el horario seleccionado.')
    return redirect(url_for('reserva.index'))

@reserva_bp.route('/mis_reservas')
@login_required
def mis_reservas():
    s = current_app.config['sirope']
    todas_reservas = list(s.load_all(Reserva))
    
    for reserva in todas_reservas:
        reserva.fecha_hora = convert_to_datetime(reserva.fecha_hora)
    
    reservas_futuras = [reserva for reserva in todas_reservas if reserva.user_id == current_user.get_id() and reserva.fecha_hora >= datetime.now()]
    reservas_antiguas = [reserva for reserva in todas_reservas if reserva.user_id == current_user.get_id() and reserva.fecha_hora < datetime.now()]
    return render_template('mis_reservas.html', reservas_futuras=reservas_futuras, reservas_antiguas=reservas_antiguas)

@reserva_bp.route('/editar/<reserva_id>', methods=['GET', 'POST'])
@login_required
def editar(reserva_id):
    s = current_app.config['sirope']
    reserva = next((r for r in s.load_all(Reserva) if r._id == reserva_id), None)

    if not reserva:
        flash('Reserva no encontrada.')
        return redirect(url_for('reserva.mis_reservas'))

    if request.method == 'POST':
        if hasattr(reserva, 'editada') and reserva.editada:
            flash('No se puede volver a editar la reserva.')
            return redirect(url_for('reserva.mis_reservas'))
        
        fecha_original = reserva.fecha_hora
        fecha_maxima_edicion = fecha_original + timedelta(days=30)
        nueva_fecha = datetime.strptime(request.form.get('fecha') + ' ' + request.form.get('hora'), '%Y-%m-%d %H:%M')

        if nueva_fecha > fecha_maxima_edicion:
            flash('La fecha de edición no puede ser más de un mes después de la fecha original.')
            return redirect(url_for('reserva.mis_reservas'))

        if nueva_fecha.hour < 12 or nueva_fecha.hour >= 22:
            flash('Las reservas solo pueden hacerse entre las 12:00 y las 22:00.')
            return redirect(url_for('reserva.editar', reserva_id=reserva_id))

        fecha_fin_reserva = nueva_fecha + timedelta(hours=2)

        num_personas = int(request.form['num_personas'])
        mesas = list(s.load_all(Mesa))
        mesas_disponibles = [mesa for mesa in mesas if mesa.capacidad >= num_personas and mesa.capacidad <= num_personas * 2]

        for mesa in mesas_disponibles:
            reservas = list(s.load_all(Reserva))
            reservas_mesa = [r for r in reservas if r.numero_mesa == mesa.numero and r.fecha_hora.date() == nueva_fecha.date()]
            disponible = True

            for r in reservas_mesa:
                reserva_fin = r.fecha_hora + timedelta(hours=2)
                if not (nueva_fecha >= reserva_fin or fecha_fin_reserva <= r.fecha_hora):
                    disponible = False
                    break
                reserva_fin2 = r.fecha_hora - timedelta(hours=2)
                if not (nueva_fecha <= reserva_fin2 or fecha_fin_reserva <= r.fecha_hora):
                    disponible = False
                    break
            
            if disponible:
                reserva.fecha_hora = nueva_fecha
                reserva.numero_mesa = mesa.numero
                reserva.num_personas = num_personas
                reserva.editada = True  # Marcar como editada
                s.save(reserva)
                flash('Reserva actualizada correctamente.')
                return redirect(url_for('reserva.mis_reservas'))

        flash('No hay mesas disponibles en el horario seleccionado.')
        return redirect(url_for('reserva.mis_reservas'))

    return render_template('editar_reserva.html', reserva=reserva)
