from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm, RoomSelectForm


@main.route('/')
def index():
    """Login form to authentication step."""
    form = LoginForm()
    return render_template('index.html', form=form)


@main.route('/chat/<room>')
def chat(room):
    """Chat room. The user's name and room must be stored in
    the session."""
    if room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', room=room)

@main.route('/dump')
def dump():
    """Server dumps"""
    return render_template('dump.html')

@main.route('/room')
def select_room():
    """Room entering form"""
    form = RoomSelectForm()
    return render_template('room.html', form=form)
