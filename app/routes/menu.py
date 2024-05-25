from flask import Blueprint, render_template
import sirope
from ..models.plato import Plato
from ..models.menu import Menu

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/menu')
def index():
    s = sirope.Sirope()
    platos = list(s.load_all(Plato))
    menus = list(s.load_all(Menu))

    for menu in menus:
        menu.platos = [s.find_first(Plato, lambda p: p._id == plato_id) for plato_id in menu.platos_ids]

    return render_template('menu.html', platos=platos, menus=menus)
