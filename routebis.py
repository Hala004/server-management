#cette page permet de créer un user sur un serveur
#fait
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
    # il faut faire le choix
    # var_entre = request.form()          recupère une entrer sur l'interface celle pour le choix d'un affichage instatané et celle non
    # if var_entre == "instant":
    device.find_prompt()
    output = device.send_command("ps -aux | awk {'print $1 \"        \" $3 \"        \" $4 \"        \" $11'}")
    # elif
    # on fait appelle à une fonction qui fait l'affichage par soit par date et heure, par date ou soit par heure
    #il faut définir ces fonctions(requètes SQL)
    # affiche_date_heure()
    # elif
    # affiche_date()
    # elif
    # affiche_heure()

    f = output.replace('\n', ',')
    l = f.split(',')

    return render_template('interface.html', message=l)




#pas encore fait
#cette page fait l'affichage instantantané des info sur le cpu
@app.route('/info_cpu/')
def info_cpu():
    device.find_prompt()
    output = device.send_command("cat /proc/cpuinfo | head -9")
    f = output.replace('\n',',')
    l = f.split(',')
    return render_template('cpu_inf.html', info=l)

#pas encore fait
#la fonction d'affichage à utiliser ici est affiche_tb_disc
#la page qui permet d'afficher l'état des partitions instantanement et dans le temps, elle également doit conternir des instruction suplémentaire pour l'affichage dans le temps
@app.route('/etat_partitions')
def etat_partitions():
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

##################################################
# Connection à un serveur
@app.route('/connectServer', methods=['GET', 'POST'])
@login_required
def connectServer():
    global device
    form = classes.Connection_serv()
    if form.validate_on_submit():
        nom_server = form.name_server.data

        obj2 = database.sesh.query(database.Server).filter(database.Server.name_server.ilike(nom_server)).all()

        #if current_user.id_user == obj2.id_owner:
        if obj2 == None:
            flash("This name does not exist")
            adr = " "
        else:
            for ipp in obj2:
                adr = ipp.ip_address

        username = form.username.data
        mot_de_passe = form.password.data

        if adr == " ":
            flash("This Server does not exist!")
        else:
            device = ConnectHandler(device_type='linux', ip=adr, username=username, password=mot_de_passe)
            functions.planification(device)
            functions.thread_fonc(device)
            return redirect(url_for("dashboard2"))
        #else:
           # return "<h1> You are not authorized to have access to this server! </h1>"

    return render_template('connectServer.html', form=form)


###########################################################################
###############################################################################

if "username" in session and "password" in session and "name_server" in session:
    username1 = session["username"]
    password1 = session["password"]
    name_server1 = session["name_server"]

obj2 = database.sesh.query(database.Server).filter(database.Server.name_server.ilike(name_server1)).all()
# if current_user.id_user == obj2.id_owner:
if obj2 == None:
    flash("This name does not exist")
    adr = " "
else:
    for ipp in obj2:
        adr = ipp.ip_address
device = ConnectHandler(device_type='linux', ip=adr, username=username1, password=password1)
