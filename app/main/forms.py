from flask_wtf import Form
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import Required


class LoginForm(Form):
    """Accepts a nickname and a password."""
    name = StringField('Name', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])

class RoomSelectForm(Form):
    """Accepts a nickname and a password."""
    room = StringField('Room', validators=[Required()])
    submit = SubmitField('Enter Chatroom')
