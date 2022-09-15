class User(FlaskForm):
    nom = StringField("Nom d'utilisateur", validators=[DataRequired()])
    mot_de_passe = StringField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Créer ')

class Suppression(FlaskForm):
    nom = StringField("Nom d'utilisateur", validators=[DataRequired()])
    submit = SubmitField('Supprimer ')

class connected_users(FlaskForm):
    #Affichage direct

class mem_stat(FlaskForm):
    #not yet (Radio buttons+calendrier),time related

class CPU_stat(FlaskForm):
    # not yet (Radio buttons+calendrier),time related

class View_partition(FlaskForm):
    # not yet (Radio buttons+calendrier),time related

class View_DIR_content(FlaskForm):
    d = StringField("le nom du répertoire", validators=[DataRequired()])
    submit = SubmitField("L'état de ce répertoire ")

class CPU_LOAD(FlaskForm):
    # not yet (Radio buttons+calendrier),time related

class PROC_BY_USER(FlaskForm):
    # not yet (Radio buttons+calendrier),time related
    nom = StringField("Nom d'utilisateur", validators=[DataRequired()])
    # submit = SubmitField('Afficher ')

class PROC_PID(FlaskForm):
    cmd = StringField("le nom du démon ", validators=[DataRequired()])
    submit = SubmitField("Afficher le PID de ce processus")

class PROC_PID_PPID(FlaskForm):
    # not yet (Radio buttons+calendrier),time related
    #submit = SubmitField("Afficher les processus parents et  fils ")

class KILL_PROC(FlaskForm):
    cmd = StringField("le nom du démon ", validators=[DataRequired()])
    submit = SubmitField("Arrêter ce processus")

class NET_stat(FlaskForm):
    #affichage direct
