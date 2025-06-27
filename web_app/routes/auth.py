from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from web_app.models import User
from web_app.extensions import db
from web_app.forms import LoginForm, RegisterForm, LogoutForm

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('views.admin_base' if user.is_admin else 'views.user_base'))
        else:
            flash('Invalid email or incorrect password. Please try again.', category='error')
    else:
        if request.method == 'POST':
            for errors in form.errors.values():
                for error in errors:
                    flash(error, category='error')

    return render_template("login.html", user=current_user, form=form)

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    form = LogoutForm()
    if form.validate_on_submit():
        logout_user()
        flash('Logged out successfully.', category='success')
        return redirect(url_for('auth.login'))
    else:
        flash('Invalid logout attempt (CSRF token missing or invalid).', category='error')
        return redirect(url_for('views.user_base'))

@auth.route('/register', methods=['GET', 'POST'])
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        password1 = form.password1.data

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered.', category='error')
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                password=generate_password_hash(password1, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.user_base'))
    
    elif request.method == 'POST':
        for field_errors in form.errors.values():
            for error in field_errors:
                flash(error, category='error')

    return render_template("register.html", user=current_user, form=form)