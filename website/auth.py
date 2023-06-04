from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)

BANLIST = []


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                if current_user.id in BANLIST:
                    logout_user()
                    flash('You are banned from FlashForum!', category='error')
                    return redirect(url_for('auth.login'))
                flash('Logged in!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password!', category="error")
        else:
            flash("Account does not exist!", category='error')
        
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already registered!', category='error')
        elif len(email) < 4:
            flash("Email is too short!", category='error')
        elif password1 != password2:
            flash("Passwords don't match!", category='error')
        elif len(password1) < 7:
            flash("Password is too short!", category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash("Account created!", category='success')
            return redirect(url_for('views.home'))
    
    return render_template("sign_up.html", user=current_user)

@auth.route('/banned', methods=["GET", "POST"])
def banned():
    return render_template("banned.html", user=current_user)

@auth.route('/ban-user/<user_id>', methods=['POST'])
def ban_user(user_id):
    user = User.query.get(user_id)
    if user:
    
        user.banned = True
        db.session.commit()
    
    return redirect(url_for('views.home'))