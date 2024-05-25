from flask import Flask, render_template
from flask_login import LoginManager
from sirope.sirope_main import Sirope
from .models.user import User
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Crear instancia de Sirope
    s = Sirope()

    @login_manager.user_loader
    def load_user(user_id):
        return s.find_first(User, lambda u: u.email == user_id)  

    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes.reserva import reserva_bp as reserva_blueprint
    app.register_blueprint(reserva_blueprint)

    from .routes.menu import menu_bp as menu_blueprint
    app.register_blueprint(menu_blueprint)

    from .routes.calificacion import calificacion_bp as calificacion_blueprint
    app.register_blueprint(calificacion_blueprint)  

    from .routes.propuesta_plato import propuesta_bp
    app.register_blueprint(propuesta_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    app.config['sirope'] = s

    return app
