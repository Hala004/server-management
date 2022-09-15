from web_flask.partie_flask import app
from flask import render_template, request, redirect, url_for
from Gestion_Ram_et_Disc_dur.planification import planification
from netmiko import *
from Gestion_Ram_et_Disc_dur.Annexe_de_routes import create_user, add_server, drop_server, adresse_ip, Ajout, Connection_serv, User, Suppression
from Gestion_Ram_et_Disc_dur.remplissage_table import thread_fonc
from web_flask.models import *


#pour exécuter lancer le fichier partie_flask

@app.route('/', methods=['GET','POST'])     #page principale de l'application
def index():
    return render_template('Page_d_accueil.html')

@app.route('/connection_server/',methods=['GET','POST'])    #cette page permet de ce connecter à un serveur
def connection_server():
    global device
    form = Connection_serv()
    if form.validate_on_submit():
        nom_server = form.Nom_du_serveur.data
        adr = adresse_ip(nom_server)
        username = form.Username.data
        mot_de_passe = form.Mot_de_passe.data
        if adr == " ":
            return "<h2> ce serveur n'exite pas encore voulez vous le créer?</h2>"
        else:
            device = ConnectHandler(device_type='linux', ip=adr, username=username, password=mot_de_passe)
            planification(device)
            thread_fonc(device)
            return redirect(url_for("index"))
    return render_template('formulaire2.html', form=form)

#fait
@app.route('/ajout_server/',methods=['GET','POST'])  #cette page permet de faire l'ajout d'un serveur
def ajout_server():

    form = Ajout()
    if form.validate_on_submit():
        nom = form.Nom_du_serveur.data
        add_ip = form.Adresse_ip.data
        sortie = add_server(nom, add_ip)
        if sortie == " ":
            return redirect('/connection_server/')    #vous pourez refaire la redirection pour l'instant elle génère un message comme retour vide surement vous avez une autre méthode pour les redirection
        else:
            return sortie
    return render_template('formulaire1.html', form=form)


#cette page permet de créer un user sur un serveur
@app.route('/create_users/')
def create_users():
    form = User()
    if form.validate_on_submit():
        nom = form.Nom.data
        mot_de_passe = form.Mot_de_passe.data
        output = create_user(nom, mot_de_passe)
        if len(output[0]) == 0:
            return "<p>commande exécuter avec succès</p>"

        else:
            if output[0] != " ":
                return output[0]
    return render_template('formulaire.html', form=form)


# fait
@app.route('/supprimer_serveur/', methods=['POST'])    #cette page permet de supprimer un serveur
def supprimer_serveur():
    form = Suppression()
    if form.validate_on_submit():
        nom = form.Nom_du_serveur.data
        sortie = drop_server(nom)
        if sortie != " ":
            return "<p> serveur supprimer avec succès</p>"
        else:
            return "<p> Echec de Suppression, serveur inexistant!!</p>"
    return render_template('formulaire3.html', form=form)

#pas encore fait
# cette page permet d'afficher les utilisateur qui sont connectés
@app.route('/utilisateur_connecte/')
def utilisateur_connecte():
    output = affichage_tb_user()
    return output

#pas encore fait
#cette page permet l'affichage de l'état de la mémoire ram, elle fait l'affichage dans le temps et instantanée
# la fonction d'affichage à utiliser ici est affichage_tb_mem
@app.route('/etat_memoire/')
def etat_memoire():

    #var_entre = request.form()          recupère une entrer sur l'interface celle pour le choix d'un affichage instatané et celle non
    #if var_entre == "instant":
    device.find_prompt()
    output = device.send_command("ps -aux | awk {'print $1 \"        \" $3 \"        \" $4 \"        \" $11'}")
    #elif
        #on fait appelle à une fonction qui fait l'affichage par soit par date et heure, par date ou soit par heure
        #affiche_date_heure()
    #elif
        #affiche_date()
    #elif
        #affiche_heure()

    f = output.replace('\n',',')
    l = f.split(',')

    return render_template('interface.html', message=l)

#pas encore fait
@app.route('/info_cpu/')
def info_cpu():       #cette page fait l'affichage instantantané des info sur le cpu
    device.find_prompt()
    output = device.send_command("cat /proc/cpuinfo | head -9")
    f = output.replace('\n',',')
    l = f.split(',')
    return render_template('cpu_inf.html', info=l)

#pas encore fait
@app.route('/etat_partitions')   #la fonction d'affichage à utiliser ici est affiche_tb_disc
def etat_partitions():    #la page qui permet d'afficher l'état des partitions instantanement et dans le temps, elle également doit conternir des instruction suplémentaire pour l'affichage dans le temps
    device.find_prompt()
    output = device.send_command("df -h")
    f = output.replace('\n', ',')
    l = f.split(',')

    return render_template('partition_info.html', message=l)

#pas encore fait
@app.route('/etat_disc/')  #la page permettant l'affichage du volume d'un dossier ou d'un fichier, l'affichage est instantanée
def etat_disc():
    device.find_prompt()
    d = '/home/lferdinand' # input('donner le repertoire dont vous désirez consulter l\'\état: ') nécessite une entrée de l'interface
    output = device.send_command("du -s -h %s" % d)


    return (output)

#pas encore fait
@app.route('/charge_moyenne_cpu_instantanee/')   #cette page permet d'afficher la charge moyenne du système, elle fait l'affichage instanté et celle dans le temps
def charge_moyenne_cpu_instantanee():   #la fonction d'affichage bd à utiliser ici est affichage_tb_cpu
    device.find_prompt()
    output = device.send_command(" iostat | tail -8")
    f = output.replace('\n', ',')
    l = f.split(',')

    return render_template('charge_moyenne_cpu.html', message=l)

#Pas encore fait
@app.route('/processus_user/')     #cette page permet de faire l'affichage instannée des processus et des commandes lancées par un utilisateur particulier
def processus_user():
    nom = 'lferdinand'  #input('entrer le nom du user à inspecter: ') nécessite un input de l'interface
    device.find_prompt()
    output = device.send_command(" ps -u %s"% nom)
    f = output.replace('\n', ',')
    l = f.split(',')

    return render_template('proc_user.html', message=l)

#Pas encore fait
@app.route('/PID_cmd')  #cette page permet de faire l'affichage du pid d'un processus en donnant son nom
def PID_cmd():
    cmd ='sshd'  #input('entrer le nom demon dont vous désirez connaître le PID: ') nécessite un input de l'interface
    device.find_prompt()
    output = device.send_command(" pgrep  -l %s" % cmd)

    return (output)

#Pas encore fait
@app.route('/affichage_PID_PPID/')    # cette page permet l'affichage des processus parents et de leurs fils, l'affichage est instantanée
def affichage_PID_PPID():

    device.find_prompt()
    output = device.send_command("ps -exjH")

    return output

#Pas encore fait
@app.route('/kill_pross/')    #cette page est celle qui permet à l'admin de tuer un processus
def kill_pross():
    cmd = 'sshd' # input('entrer le pid du démon que vous voulez arrêter: ') nécessite un input de l'interface
    device.find_prompt()
    device.send_command(" kill  -9 %s" % cmd)

    return ("processus arrêté avec succès")

#pas encore fait
@app.route('/network_stat/')    # cette page permet de faire le contrôle du flux tcp
def network_stat():
    device.find_prompt()
    output = device.send_command("netstat -an --tcp --program")

    return output
