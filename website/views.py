from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from .auth import BANLIST
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, logout_user, login_required, current_user

admins = [1]

auth = Blueprint('auth', __name__)
views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    if current_user.id in BANLIST:
        logout_user()
        flash('You are banned from FlashForum!', category='error')
        return redirect(url_for('auth.banned'))
    
    if request.method == "POST":
        note = request.form.get('note')

        if len(note) < 1:
            flash("Your post is too short!", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Posted!', category="success")

    notes = Note.query.all()
    return render_template("home.html", user=current_user, notes=notes, admins=admins)

@views.route('/remove-note/<int:note_id>', methods=['POST'])
@login_required
def remove_note(note_id):
    note = Note.query.get_or_404(note_id)

    if note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        flash('Your post was removed successfully!', category='success')
    elif current_user.id in admins:
        db.session.delete(note)
        db.session.commit()
        flash('Admin-removed successfully!', category='error')
    else:
        flash('This is not your post!', category='error')

    return redirect(url_for('views.home'))

@views.route('/admin', methods=["GET", "POST"])
@login_required
def admin():
    ban_string = ""
    
    if request.method == "POST":
        user_id = request.form.get('user_id')
        flash("Variable " + user_id + " has been created!", category='success')
        
    
    return render_template("admin.html", user=current_user, ban_value=ban_string, admins=admins)


