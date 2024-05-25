from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        s = current_app.config['sirope']
        user = s.find_first(User, lambda u: u.email == email)
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Correo electrónico o contraseña incorrectos')
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        s = current_app.config['sirope']
        user = s.find_first(User, lambda u: u.email == email)
        if user:
            flash('El correo electrónico ya está registrado')
        else:
            new_user = User(username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))
            s.save(new_user)
            login_user(new_user)
            return redirect(url_for('index'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
