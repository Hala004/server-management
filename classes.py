from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, RadioField
from wtforms.validators import InputRequired, Length, DataRequired
from wtforms.fields.html5 import DateField, TimeField


# Les différents champs à remplir
#fait
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

#fait
class RegisterForm(FlaskForm):
    name_server = StringField('Server Name', validators=[InputRequired(), Length(max=50)])
    ip_address = StringField('IP Address', validators=[InputRequired(), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

# les champs à remplir pour ajouter un serveur
class Ajout(FlaskForm):
    name_server = StringField('Server Name', validators=[DataRequired()])
    ip_address = StringField('IP Address', validators=[DataRequired()])


# les champs à remplir pour supprimer un srv
class Suppression(FlaskForm):
    name_server = StringField('Server Name', validators=[DataRequired()])


# les champs à remplir pour se connecter à un serveur, il faut donner de plus le nom et mdp du compte avec lequel on se connectera au niveau du srv
class Connection_serv(FlaskForm):
    name_server = StringField('Server Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

#Les champs à remplir pour ajouter un utilisateur au niveau du serveur
class create_User(FlaskForm):
    name_user = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])

#Les champs à remplir pour supprimer un utilisateur au niveau d'un serveur
class delete_User(FlaskForm):
    name_user = StringField("Nom d'utilisateur", validators=[DataRequired()])


#class connected_users(FlaskForm):
    #name_server = StringField("Server name", validators=[DataRequired()])

class mem_stat(FlaskForm):
    #date = StringField('Date', validators=[DataRequired()])
    #heure = StringField('Time', validators=[DataRequired()])
    #date_heure = DateTimeField('Date and time', format='%Y-%m-%d %H:%M:%S')
    choice = RadioField('By:', choices=[('1', 'Date'), ('2', 'Time'), ('3', 'Date and time'), ('4', 'Real Time')])


class CPU_stat(FlaskForm):
    #date = StringField('Time', validators=[DataRequired()])
    #date_heure = DateTimeField('Date and time', format='%Y-%m-%d %H:%M:%S')
    choice = RadioField('By:', choices=[('1', 'Date'), ('2', 'Time'), ('3', 'Date and time'), ('4', 'Real time')])
    # submit = SubmitField('Afficher ')


class View_partition(FlaskForm):
    #date = StringField('Date', validators=[DataRequired()])
    #heure = StringField('time', validators=[DataRequired()])
    #date_heure = DateTimeField('Date and time', format='%Y-%m-%d %H:%M:%S')
    choice = RadioField('By:', choices=[('1', 'Date'), ('2', 'Time'), ('3', 'Date and time'), ('4', 'Real time')])
    # submit = SubmitField('Afficher ')

class View_DIR_volume(FlaskForm):
    d = StringField("Directory name", validators=[DataRequired()])


class CPU_LOAD(FlaskForm):
    #date = StringField('Date', validators=[DataRequired()])
    #heure = StringField('Time', validators=[DataRequired()])
    #date_heure = DateTimeField('Date and time', format='%Y-%m-%d %H:%M:%S')
    choice = RadioField('By:', choices=[('1', 'Date'), ('2', 'Time'), ('3', 'Date and time'), ('4', 'Real time')])
    # submit = SubmitField('Afficher ')

class PROC_BY_USER(FlaskForm):
    name_user = StringField("Username", validators=[DataRequired()])
    #date = DateField('Date', format='%Y-%m-%d')
    #heure = TimeField('Heure', format='%H:%M:%S')
    #date_heure = DateTimeField('Date et heure', format='%Y-%m-%d %H:%M:%S')
    #choice = RadioField('Par:', choices=[('1', 'Date'), ('2', 'Heure'), ('3', 'Date & Heure'), ('4', 'Temps réel')])

    # submit = SubmitField('Afficher ')

# connaitre le PID d'un processus
class PROC_PID(FlaskForm):
    cmd = StringField("Daemon name ", validators=[DataRequired()])

class PROC_PID_PPID(FlaskForm):
    #date = StringField('Date', validators=[DataRequired()])
    #heure = StringField('Time', validators=[DataRequired()])
    #date_heure = DateTimeField('Date and time', format='%Y-%m-%d %H:%M:%S')
    choice = RadioField('By:', choices=[('1', 'Date'), ('2', 'Time'), ('3', 'Date and time'), ('4', 'Real time')])

    #submit = SubmitField("Afficher les processus parents et  fils ")

# champ à remplir par le PID du démon à tuer
class KILL_PROC(FlaskForm):
    cmd = StringField("PID of daemon", validators=[DataRequired()])


class connected_user(FlaskForm):
    #date = StringField('Date', validators=[DataRequired()])
    #heure = StringField('Time', validators=[DataRequired()])
    #date_heure = DateTimeField('Date and time', format='%Y-%m-%d %H:%M:%S')
    choice = RadioField('By:', choices=[('1', 'Date'), ('2', 'Time'), ('3', 'Date and time'), ('4', 'Real time')])

class dateRamf(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])

class timeRamf(FlaskForm):
    heure = StringField('Time', validators=[DataRequired()])

class datetimeRamf(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    heure = StringField('Time', validators=[DataRequired()])

class dateViewPartitionf(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])

class timeViewPartitionf(FlaskForm):
    heure = StringField('Time', validators=[DataRequired()])

class datetimeViewPartitionf(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    heure = StringField('Time', validators=[DataRequired()])

class dateViewAverageCpuf(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])

class timeViewAverageCpuf(FlaskForm):
    heure = StringField('Time', validators=[DataRequired()])

class datetimeViewAverageCpuf(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    heure = StringField('Time', validators=[DataRequired()])


class dateShowConnectf(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])

class timeShowConnectf(FlaskForm):
    heure = StringField('Time', validators=[DataRequired()])

class datetimeShowConnectf(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    heure = StringField('Time', validators=[DataRequired()])


class changeAddress(FlaskForm):
    name_server = StringField('Server Name', validators=[DataRequired()])
    ip_address = StringField(' New Ip Address', validators=[DataRequired()])

#class NET_stat(FlaskForm):
    #name_server = StringField("Server name", validators=[DataRequired()])
    #affichage direct