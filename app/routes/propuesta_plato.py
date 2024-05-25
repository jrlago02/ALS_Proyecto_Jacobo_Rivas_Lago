from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from ..models.propuesta_plato import PropuestaPlato

propuesta_bp = Blueprint('propuesta', __name__)

@propuesta_bp.route('/proponer_plato', methods=['GET', 'POST'])
@login_required
def proponer_plato():
    s = current_app.config['sirope']

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        precio_max = float(request.form['precio_max'])
        nota = float(request.form['nota'])
        
        propuesta = PropuestaPlato(user_id=current_user.get_id(), titulo=titulo, descripcion=descripcion, precio_max=precio_max, nota=nota)
        s.save(propuesta)
        
        flash('Propuesta enviada correctamente. ¡Gracias por tu colaboración!')
        return redirect(url_for('propuesta.proponer_plato'))
    
    return render_template('proponer_plato.html')

@propuesta_bp.route('/mis_propuestas')
@login_required
def mis_propuestas():
    s = current_app.config['sirope']
    propuestas = [p for p in s.load_all(PropuestaPlato) if p.user_id == current_user.get_id()]
    return render_template('mis_propuestas.html', propuestas=propuestas)
