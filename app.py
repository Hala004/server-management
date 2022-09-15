from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_bootstrap import Bootstrap
from netmiko import ConnectHandler
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import classes
import database
import functions
from sqlalchemy import and_
from flask import Response, Flask
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from matplotlib.figure import Figure
from netmiko import *
from matplotlib import pylab, pyplot
from flask import g
from datetime import date, datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
bootstrap = Bootstrap(app)
app.secret_key = "hello"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id_user):
    return database.sesh.query(database.User).get(int(id_user))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = classes.LoginForm()
    message = ''
    if form.validate_on_submit():
        user = database.sesh.query(database.User).filter_by(username=form.username.data).first()
        if user != None:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        message = 'Invalid username or password'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form , data=message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = classes.RegisterForm()
    message = ""

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = database.sesh.query(database.User).filter_by(username=form.username.data).first()
        if user!= None:
           message = "This User already exist, try another credentials please!"
        else:
            new_user = database.User(username=form.username.data, password=hashed_password)
            database.sesh.add(new_user)
            database.sesh.commit()
            alpha = database.sesh.query(database.User).filter_by(username=form.username.data).first()
            new_server = database.Server(name_server=form.name_server.data, ip_address=form.ip_address.data)
            new_server.id_owner = alpha.id_user
            database.sesh.add(new_server)
            database.sesh.commit()

            message = "New user and server have been created!"
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form ,data = message)


@app.route('/dashboard')
@login_required
def dashboard():
    current_user.username
    s_name = []
    s_ip = []
    s_id = []
    admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
    admin_id = admin.id_user
    serveurs = database.sesh.query(database.Server).filter(database.Server.id_owner.ilike(admin_id)).all()
    for i in serveurs:
        s_name.append(i.name_server)
        s_ip.append(i.ip_address)
        s_id.append(i.id_server)

    return render_template('dashboard.html', name=current_user.username, data1=s_name, data2=s_ip, data3=s_id, beta=len(s_name))


@app.route('/logout')
@login_required
def logout():
    session.pop("username", None)
    session.pop("password", None)
    session.pop("name_server", None)
    logout_user()
    return redirect(url_for('index'))

# Connection à un serveur
@app.route('/connectServer', methods=['GET', 'POST'])
@login_required
def connectServer():
    global device
    form = classes.Connection_serv()
    adr = ""

    if form.validate_on_submit():
        nom_server = form.name_server.data

        obj2 = database.sesh.query(database.Server).filter(database.Server.name_server.ilike(nom_server)).all()

        #if current_user.id_user == obj2.id_owner:
        if obj2 == None:
            return "This name does not exist"
            adr = " "
        else:
            for ipp in obj2:
                adr = ipp.ip_address

        username = request.form["username"]
        password = request.form["password"]
        name_server = request.form["name_server"]
        session["username"] = username
        session["password"] = password
        session["name_server"] = name_server

        username = form.username.data
        mot_de_passe = form.password.data

        if adr == " ":
            return "This Server does not exist!"
        else:
            device = ConnectHandler(device_type='linux', ip=adr, username=username, password=mot_de_passe)
            output = device.send_command(" who | awk {'print $1'} ")
            output1 = device.send_command("who | awk {'print $3'}")
            output2 = device.send_command("who | awk {'print $4'}")
            x = output
            x2 = output1
            x3 = output2
            xl = x.replace('\n', ',')
            xl1 = x2.replace('\n', ',')
            xl2 = x3.replace('\n', ',')
            xb = xl.split(',')
            xb1 = xl1.split(',')
            xb2 = xl2.split(',')
            for i in range(len(xb) - 1):
                xb[i].rstrip('\n')
                xb1[i].rstrip('\n')
                xb2[i].rstrip('\n')

            for i in range(len(xb)-1):
                obj1 = database.sesh.query(database.USERS) \
                    .filter(database.USERS.login.ilike(xb[i])) \
                    .all()

                obj2 = database.sesh.query(database.USERS) \
                    .filter(database.USERS.date.ilike(xb1[i])) \
                    .all()

                obj3 = database.sesh.query(database.USERS) \
                    .filter(database.USERS.temp.ilike(xb2[i])) \
                    .all()

                if (obj1 == [] or obj2 == [] or obj3 == []):
                    ob = database.USERS(login=xb[i], date=xb1[i], temp=xb2[i], server_user=nom_server)
                    database.sesh.add(ob)
                    database.sesh.commit()
            g.device = device
            functions.planification(g.device)
            functions.thread_fonc(g.device, nom_server)
            #functions.affiche_user(g.device, nom_server)
            return redirect(url_for("dashboard2"))
        #else:
           # return "<h1> You are not authorized to have access to this server! </h1>"

    return render_template('connectServer.html', form=form)

# Suppression d'un serveur
@app.route('/deleteServer', methods=['GET','POST'])
@login_required
def deleteServer():

    form = classes.Suppression()
    message = ""
    if form.validate_on_submit():
        name = form.name_server.data
        obj3 = database.sesh.query(database.Server).filter(database.Server.name_server.ilike(name)).all()
        if obj3 != []:
            database.sesh.query(database.Server).filter(database.Server.name_server.ilike(name)).delete(synchronize_session=False)
            database.sesh.commit()
            message = "Your Server has been deleted successfully!"
        else:
            message = "Server does not exist, try another name please!"

    return render_template('deleteServer.html', form=form , data=message)


# Ajout d'un serveur
@app.route('/addServer', methods=['GET' , 'POST'])
@login_required
def addServer():

    form = classes.Ajout()
    name = current_user.username
    alpha = database.sesh.query(database.User).filter_by(username=name).first()
    id_own = alpha.id_user
    message = ""
    if form.validate_on_submit():
        name = form.name_server.data
        add_ip = form.ip_address.data

        obj0 = database.sesh.query(database.Server).filter(database.Server.name_server.ilike(name)).all()

        obj1 = database.sesh.query(database.Server).filter(database.Server.ip_address.ilike(add_ip)).all()

        if (obj0 == [] and obj1 == []):
            obj = database.Server(name, add_ip)
            obj.id_owner = id_own
            database.sesh.add(obj)
            database.sesh.commit()
            message = "Your server has been added"
        else:
            message = "This name already exists, try another name please!"

    return render_template('addServer.html', form=form , data = message)


# faite
@app.route('/createUserf', methods=['GET' , 'POST'])
@login_required
def createUserf():
    form = classes.create_User()
    message = ""
    if form.validate_on_submit():
        name_user = form.name_user.data
        password = form.password.data
        if "username" in session and "password" in session and "name_server" in session:
            username1 = session["username"]
            password1 = session["password"]
            name_server1 = session["name_server"]

        obj2 = database.sesh.query(database.Server).filter(database.Server.name_server.ilike(name_server1)).all()
        # if current_user.id_user == obj2.id_owner:
        if obj2 == None:
            message = "This name does not exist"
            adr = " "
        else:
            for ipp in obj2:
                adr = ipp.ip_address

        device = ConnectHandler(device_type='linux', ip=adr, username=username1, password=password1)

        output = functions.create_user(name_user, password, device)
        if len(output[0]) == 0:
            message = "The user has been created successfully!"
        else:
            if output[0] != " ":
                message = f"{output[0]} "

    return render_template('createUserf.html', form=form, data=message)

# faite
@app.route('/deleteUserf', methods=['GET' , 'POST'])
@login_required
def deleteUserf():
    form = classes.delete_User()
    message = ""
    if form.validate_on_submit():
        nom = form.name_user.data
        if "username" in session and "password" in session and "name_server" in session:
            username1 = session["username"]
            password1 = session["password"]
            name_server1 = session["name_server"]

        obj2 = database.sesh.query(database.Server).filter(database.Server.name_server.ilike(name_server1)).all()
        # if current_user.id_user == obj2.id_owner:
        if obj2 == None:
            message = "This name does not exist"
            adr = " "
        else:
            for ipp in obj2:
                adr = ipp.ip_address
        device = ConnectHandler(device_type='linux', ip=adr, username=username1, password=password1)

        output = functions.delete_user(nom, device)
        if len(output) == 0 :
            message = "The user has been deleted successfully!"

        else:
            if output != " ":
                message = f"{output} "

    return render_template('deleteUserf.html', form=form, data=message)

# faite
@app.route('/displayParentsf', methods=['GET' , 'POST'])
@login_required
def displayParentsf():
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
    device.find_prompt()
    output = device.send_command("ps -exjH ")
    #est ce que cette commande est juste, ou je dois laisser la fonction avec return output?
    return f"<h1> {output} </h1>"

    return render_template('displayParentsf.html')


@app.route('/displayPidf', methods=['GET' , 'POST'])
@login_required
def displayPidf():
    form = classes.PROC_PID()
    if form.validate_on_submit():
        cmd = form.cmd.data
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
        device.find_prompt()
        output = device.send_command(" pgrep  -l %s " % cmd)
        return f"<h1> {output} </h1>"

    return render_template('displayPidf.html', form=form)

# faite
@app.route('/killProcessesf', methods=['GET', 'POST'])
@login_required
def killProcessesf():
    form = classes.KILL_PROC()
    if form.validate_on_submit():
        cmd = form.cmd.data
        if "username" in session and "password" in session and "name_server" in session:
            username1 = session["username"]
            password1 = session["password"]
            name_server1 = session["name_server"]

        obj2 = database.sesh.query(database.Server).filter(database.Server.name_server.ilike(name_server1)).all()
        # if current_user.id_user == obj2.id_owner:
        if obj2 == None:
            return "<h1>This name does not exist</h1>"
            adr = " "
        else:
            for ipp in obj2:
                adr = ipp.ip_address
        device = ConnectHandler(device_type='linux', ip=adr, username=username1, password=password1)

        device.find_prompt()
        output = device.send_command(" kill  -9 %s" % cmd)
        if output == "Killed":
            return "<h1>Daemon killed successfully!</h1>"
        else:
            return "<h1> This PID does not exist! <br> Verify your PID here <a href= '/displayParentsf'> Display </a> </h1>"

    return render_template('killProcessesf.html', form=form)


@app.route('/showConnectf', methods=['GET', 'POST'])
@login_required
def showConnectf():
    form = classes.connected_user()
    message = ""
    if form.validate_on_submit():
        user_choice = form.choice.data
        #date = form.date.data
        #time = form.heure.data
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
        if user_choice == "4":
            device.find_prompt()
            functions.affiche_user(device, name_server1)
            output = device.send_command(" users ")
            #x = output.replace(' ', '\n')
            message = f"{output}"
        elif user_choice == "1":
            return redirect(url_for("dateShowConnectf"))
        elif user_choice == "2":
            return redirect(url_for("timeShowConnectf"))
        elif user_choice == "3":
            return redirect(url_for("datetimeShowConnectf"))

    return render_template('showConnectf.html', form=form, data=message)

@app.route('/timeShowConnectf', methods=['GET', 'POST'])
@login_required
def timeShowConnectf():
    form = classes.timeShowConnectf()
    login = []
    date = []
    temp = []
    if form.validate_on_submit():
        time = form.heure.data
        if "name_server" in session:
            name_server1 = session["name_server"]

        admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
        admin_id = admin.id_user
        chosen_server_connected_users = database.sesh.query(database.USERS).filter(
            and_(database.Server.id_owner.ilike(admin_id)
                 , database.USERS.server_user == name_server1, database.USERS.temp == time))
        for i in chosen_server_connected_users:
            login.append(i.login)
            date.append(i.date)
            temp.append(i.temp)

    return render_template('timeShowConnectf.html', form=form, login=login, date=date, temp=temp)


@app.route('/dateShowConnectf', methods=['GET', 'POST'])
@login_required
def dateShowConnectf():
    form = classes.dateShowConnectf()
    login = []
    date = []
    temp = []
    if form.validate_on_submit():
        date1 = form.date.data
        if "name_server" in session:
            name_server1 = session["name_server"]

        admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
        admin_id = admin.id_user
        chosen_server_connected_users = database.sesh.query(database.USERS).filter(
            and_(database.Server.id_owner.ilike(admin_id)
                 , database.USERS.server_user == name_server1, database.USERS.date == date1))
        for i in chosen_server_connected_users:
            login.append(i.login)
            date.append(i.date)
            temp.append(i.temp)

    return render_template('dateShowConnectf.html', form=form, login=login, date=date, temp=temp)


@app.route('/datetimeShowConnectf', methods=['GET', 'POST'])
@login_required
def datetimeShowConnectf():
    form = classes.datetimeShowConnectf()
    login = []
    date = []
    temp = []
    if form.validate_on_submit():
        time = form.heure.data
        date1 = form.date.data
        if "name_server" in session:
            name_server1 = session["name_server"]

        admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
        admin_id = admin.id_user

        chosen_server_connected_users = database.sesh.query(database.USERS).filter(
            and_(database.Server.id_owner.ilike(admin_id), database.USERS.server_user == name_server1, database.USERS.temp == time, database.USERS.date == date1))
        for i in chosen_server_connected_users:
            login.append(i.login)
            date.append(i.date)
            temp.append(i.temp)

    return render_template('datetimeShowConnectf.html', form=form, login=login, date=date, temp=temp)

@app.route('/viewAverageCpuf', methods=['GET', 'POST'])
@login_required
def viewAverageCpuf():
    form = classes.CPU_LOAD()
    if form.validate_on_submit():
        user_choice = form.choice.data
        #date = form.date.data
        #time = form.heure.data
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
        if user_choice == "4":
            device.find_prompt()
            output = device.send_command(" iostat | tail -8")
            f = output.replace('\n', ',')
            l = f.split(',')
            return f"<h1> {l} </h1>"
        elif user_choice == "1":
            return redirect(url_for("dateViewAverageCpuf"))
        elif user_choice == "2":
            return redirect(url_for("timeViewAverageCpuf"))
        elif user_choice == "3":
            return redirect(url_for("datetimeViewAverageCpuf"))

    return render_template('viewAverageCpuf.html', form=form)

@app.route('/timeViewAverageCpuf', methods=['GET', 'POST'])
@login_required
def timeViewAverageCpuf():
    form = classes.timeViewAverageCpuf()
    user = []
    nice = []
    systeme = []
    iowait = []
    steal = []
    idele = []
    date1 = []
    heure1 = []
    if form.validate_on_submit():
        time = form.heure.data
        if "name_server" in session:
            name_server1 = session["name_server"]

        admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
        admin_id = admin.id_user

        chosen_server_CPU_information = database.sesh.query(database.CPU_Status).filter(
            and_(database.Server.id_owner.ilike(admin_id), database.CPU_Status.server_CPU == name_server1,
                 database.CPU_Status.heure1 == time))
        for i in chosen_server_CPU_information:
            user.append(i.user)
            nice.append(i.nice)
            systeme.append(i.systeme)
            iowait.append(i.iowait)
            steal.append(i.steal)
            idele.append(i.idele)
            date1.append(i.date1)
            heure1.append(i.heure1)

    return render_template('timeViewAverageCpuf.html', form=form, user=user, nice=nice, systeme=systeme, iowait=iowait, steal=steal, idele=idele, date1=date1, heure1=heure1)

@app.route('/dateViewAverageCpuf', methods=['GET', 'POST'])
@login_required
def dateViewAverageCpuf():
    form = classes.dateViewAverageCpuf()
    user = []
    nice = []
    systeme = []
    iowait = []
    steal = []
    idele = []
    date1 = []
    heure1 = []
    if form.validate_on_submit():
        date = form.date.data
        if "name_server" in session:
            name_server1 = session["name_server"]
        admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
        admin_id = admin.id_user

        chosen_server_CPU_information = database.sesh.query(database.CPU_Status).filter(
            and_(database.Server.id_owner.ilike(admin_id), database.CPU_Status.server_CPU == name_server1,
                 database.CPU_Status.date1 == date))
        for i in chosen_server_CPU_information:
            user.append(i.user)
            nice.append(i.nice)
            systeme.append(i.systeme)
            iowait.append(i.iowait)
            steal.append(i.steal)
            idele.append(i.idele)
            date1.append(i.date1)
            heure1.append(i.heure1)
    return render_template('dateViewAverageCpuf.html', form=form, user=user, nice=nice, systeme=systeme, iowait=iowait, steal=steal, idele=idele, date1=date1, heure1=heure1)

@app.route('/datetimeViewAverageCpuf', methods=['GET', 'POST'])
@login_required
def datetimeViewAverageCpuf():
    form = classes.datetimeViewAverageCpuf()
    user = []
    nice = []
    systeme = []
    iowait = []
    steal = []
    idele = []
    date1 = []
    heure1 = []
    if form.validate_on_submit():
        time = form.heure.data
        date = form.date.data
        if "name_server" in session:
            name_server1 = session["name_server"]

        admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
        admin_id = admin.id_user
        chosen_server_CPU_information = database.sesh.query(database.CPU_Status).filter(
            and_(database.Server.id_owner.ilike(admin_id), database.CPU_Status.server_CPU == name_server1,
                 database.CPU_Status.heure1 == time, database.CPU_Status.date1 == date))
        for i in chosen_server_CPU_information:
            user.append(i.user)
            nice.append(i.nice)
            systeme.append(i.systeme)
            iowait.append(i.iowait)
            steal.append(i.steal)
            idele.append(i.idele)
            date1.append(i.date1)
            heure1.append(i.heure1)

    return render_template('datetimeViewAverageCpuf.html', form=form, user=user, nice=nice, systeme=systeme, iowait=iowait, steal=steal, idele=idele, date1=date1, heure1=heure1)

@app.route('/viewCpuf', methods=['GET', 'POST'])
@login_required
def viewCpuf():

    if "username" in session and "password" in session and "name_server" in session:
        username1 = session["username"]
        password1 = session["password"]
        name_server1 = session["name_server"]

        obj2 = database.sesh.query(database.Server).filter(database.Server.name_server.ilike(name_server1)).all()
        # if current_user.id_user == obj2.id_owner:
        if obj2 == None:
            return "This name does not exist"
            adr = " "
        else:
            for ipp in obj2:
                adr = ipp.ip_address
        device = ConnectHandler(device_type='linux', ip=adr, username=username1, password=password1)
        device.find_prompt()
        output = device.send_command("cat /proc/cpuinfo | head -9")
        f = output.replace('\n', ',')
        l = f.split(',')

    return render_template('viewCpuf.html', data=l)


@app.route('/viewDirectoryf', methods=['GET' , 'POST'])
@login_required
def viewDirectoryf():
    form = classes.View_DIR_volume()
    message = ""
    if form.validate_on_submit():
        d = form.d.data
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
        device.find_prompt()
        output = device.send_command("du -s -h %s" % d)

    return render_template('viewDirectoryf.html', form=form , data = output )


@app.route('/viewPartitionf', methods=['GET', 'POST'])
@login_required
def viewPartitionf():
    form = classes.View_partition()
    l = []
    if form.validate_on_submit():
        user_choice = form.choice.data
        #date = form.date.data
        #time = form.heure.data
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
        if user_choice == "4":
            device.find_prompt()
            output = device.send_command("df -h")
            f = output.replace('\n', ',')
            f = f.replace('               ', ' ')
            f = f.replace('   ', ' ')
            f = f.replace('  ', ' ')
            f = f.replace('Mounted on', 'Mounted-on')
            f = f.replace('  ', ' ')
            #l = f.replace(' ', "<td>")
            l = f.split(',')
            #return f"<h1> {l} </h1>"
        elif user_choice == "1":
            return redirect(url_for("dateViewPartitionf"))
        elif user_choice == "2":
            return redirect(url_for("timeViewPartitionf"))
        elif user_choice == "3":
            return redirect(url_for("datetimeViewPartitionf"))

    return render_template('viewPartitionf.html', form=form, data=l)


@app.route('/timeViewPartitionf', methods=['GET', 'POST'])
@login_required
def timeViewPartitionf():
    form = classes.timeViewPartitionf()
    filesystem = []
    size = []
    used = []
    avail = []
    use_percent = []
    mount_on = []
    date2 = []
    heure2 = []
    #obj = []
    if form.validate_on_submit():
        time = form.heure.data
        if "name_server" in session:
            name_server1 = session["name_server"]

        admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
        admin_id = admin.id_user

        chosen_server_disc_info = database.sesh.query(database.disc_Status).filter(
            and_(database.Server.id_owner.ilike(admin_id), database.disc_Status.server_disc == name_server1,
                 database.disc_Status.heure2 == time))
        for i in chosen_server_disc_info:
            filesystem.append(i.filesystem)
            size.append(i.size)
            used.append(i.used)
            avail.append(i.avail)
            use_percent.append(i.use_percent)
            mount_on.append(i.mount_on)
            date2.append(i.date2)
            heure2.append(i.heure2)

    return render_template('timeViewPartitionf.html', form=form, filesystem=filesystem, size=size, used=used,avail=avail, use_percent=use_percent, mount_on=mount_on, date2=date2, heure2=heure2)


@app.route('/dateViewPartitionf', methods=['GET', 'POST'])
@login_required
def dateViewPartitionf():
    form = classes.dateViewPartitionf()
    filesystem = []
    size = []
    used = []
    avail = []
    use_percent = []
    mount_on = []
    date2 = []
    heure2 = []
    obj = []
    if form.validate_on_submit():
        date = form.date.data
        if "name_server" in session:
            name_server1 = session["name_server"]

        admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
        admin_id = admin.id_user

        chosen_server_disc_info = database.sesh.query(database.disc_Status).filter(
            and_(database.Server.id_owner.ilike(admin_id), database.disc_Status.server_disc == name_server1,
                 database.disc_Status.date2 == date))
        for i in chosen_server_disc_info:
            filesystem.append(i.filesystem)
            size.append(i.size)
            used.append(i.used)
            avail.append(i.avail)
            use_percent.append(i.use_percent)
            mount_on.append(i.mount_on)
            date2.append(i.date2)
            heure2.append(i.heure2)

    return render_template('dateViewPartitionf.html', form=form, filesystem=filesystem, size=size, used=used,avail=avail, use_percent=use_percent, mount_on=mount_on, date2=date2, heure2=heure2)


@app.route('/datetimeViewPartitionf', methods=['GET', 'POST'])
@login_required
def datetimeViewPartitionf():
    form = classes.datetimeViewPartitionf()
    obj = []
    filesystem = []
    size = []
    used = []
    avail = []
    use_percent = []
    mount_on = []
    date2 = []
    heure2 = []
    if form.validate_on_submit():
        date = form.date.data
        time = form.heure.data
        if "name_server" in session:
            name_server1 = session["name_server"]

        admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
        admin_id = admin.id_user
        chosen_server_disc_info = database.sesh.query(database.disc_Status).filter(
            and_(database.Server.id_owner.ilike(admin_id), database.disc_Status.server_disc == name_server1,
                 database.disc_Status.heure2 == time, database.disc_Status.date2 == date))
        for i in chosen_server_disc_info:
            filesystem.append(i.filesystem)
            size.append(i.size)
            used.append(i.used)
            avail.append(i.avail)
            use_percent.append(i.use_percent)
            mount_on.append(i.mount_on)
            date2.append(i.date2)
            heure2.append(i.heure2)

    return render_template('datetimeViewPartitionf.html', form=form, filesystem=filesystem, size=size, used=used,avail=avail, use_percent=use_percent, mount_on=mount_on, date2=date2, heure2=heure2)


@app.route('/viewProcessesUserf', methods=['GET', 'POST'])
@login_required
def viewProcessesUserf():
    form = classes.PROC_BY_USER()
    if form.validate_on_submit():
        nom = form.name_user.data
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
        device.find_prompt()
        output = device.send_command(" ps -u %s" % nom)
        f = output.replace('\n', ',')
        l = f.split(',')
        return f"<h1> {l} </h1>"

    return render_template('viewProcessesUserf.html', form=form)


@app.route('/viewRamf', methods=['GET' , 'POST'])
@login_required
def viewRamf():
    form = classes.mem_stat()
    if form.validate_on_submit():
        user_choice = form.choice.data

        if "username" in session and "password" in session and "name_server" in session:
            username1 = session["username"]
            password1 = session["password"]
            name_server1 = session["name_server"]

        obj2 = database.sesh.query(database.Server).filter(database.Server.name_server.ilike(name_server1)).all()

        if obj2 == None:
            flash("This name does not exist")
            adr = " "
        else:
            for ipp in obj2:
                adr = ipp.ip_address
        device = ConnectHandler(device_type='linux', ip=adr, username=username1, password=password1)
        if user_choice == "4":
            device.find_prompt()
            output = device.send_command("ps -aux | awk {'print $1 \"        \" $3 \"        \" $4 \"        \" $11'}")
            f = output.replace('\n', '<tr><th>')
            l = f.replace('       ', '<td>')
            # l = f.split(',')
            #for i in range(len(f)-1):
                #if f[i] == ' ' and f[i+1] != ' ':
                    #f[i] = "aaaaaa"

            return f"<html><head><link rel='stylesheet' href='static/tableau.css'></head><h1>RAM Status</h1><table width='800' border='1' cellspacing='0'cellpadding='0' align='center'><td>{l}</table></html>"
        elif user_choice == "1":
            return redirect(url_for("dateRamf"))
        elif user_choice == "2":
            return redirect(url_for("timeRamf"))
        elif user_choice == "3":
            return redirect(url_for("datetimeRamf"))

    return render_template('viewRamf.html', form=form)


@app.route('/viewTcpf', methods=['GET' , 'POST'])
@login_required
def viewTcpf():
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
    device.find_prompt()
    output = device.send_command("netstat -an --tcp --program")
    return f"<h1>{output}</h1>"
    return render_template('viewTcpf.html')

@app.route('/dateRamf', methods=['GET', 'POST'])
@login_required
def dateRamf():
    form = classes.dateRamf()
    memTotal = []
    memFree = []
    memAvailable = []
    buffers = []
    cached = []
    date1 = []
    heure1 = []
    #name_server1 = ""
    if form.validate_on_submit():
        date2 = form.date.data
        if "name_server" in session:
            name_server1 = session["name_server"]

        admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
        admin_id = admin.id_user

        chosen_Server_RAM_information = database.sesh.query(database.Ram_Status).filter(
            and_(database.Server.id_owner.ilike(admin_id), database.Ram_Status.date == date2,
                database.Ram_Status.server_RAM == name_server1))
        for i in chosen_Server_RAM_information:
            memTotal.append(i.MemTotal)
            memFree.append(i.MemFree)
            memAvailable.append(i.MemAvailable)
            buffers.append(i.Buffers)
            cached.append(i.Cached)
            date1.append(i.date)
            heure1.append(i.heure)

    return render_template('dateRamf.html', form=form, memTotal=memTotal, memFree=memFree, memAvailable=memAvailable, buffers=buffers, cached=cached, date1=date1, heure1=heure1)


@app.route('/timeRamf', methods=['GET', 'POST'])
@login_required
def timeRamf():
    form = classes.timeRamf()
    memTotal = []
    memFree = []
    memAvailable = []
    buffers = []
    cached = []
    date1 = []
    heure1 = []
    #name_server1 = ""
    #time = ""
    if form.validate_on_submit():
        time = form.heure.data
        if "name_server" in session:
            name_server1 = session["name_server"]

        admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
        admin_id = admin.id_user

        chosen_Server_RAM_information = database.sesh.query(database.Ram_Status).filter(
            and_(database.Server.id_owner.ilike(admin_id), database.Ram_Status.heure == time,
                database.Ram_Status.server_RAM == name_server1))
        for i in chosen_Server_RAM_information:
            memTotal.append(i.MemTotal)
            memFree.append(i.MemFree)
            memAvailable.append(i.MemAvailable)
            buffers.append(i.Buffers)
            cached.append(i.Cached)
            date1.append(i.date)
            heure1.append(i.heure)

    return render_template('timeRamf.html', form=form, memTotal=memTotal, memFree=memFree, memAvailable=memAvailable, buffers=buffers, cached=cached, date1=date1, heure1=heure1)


@app.route('/datetimeRamf', methods=['GET', 'POST'])
@login_required
def datetimeRamf():
    form = classes.datetimeRamf()
    memTotal = []
    memFree = []
    memAvailable = []
    buffers = []
    cached = []
    date1 = []
    heure1 = []
    #name_server1 = ""
    if form.validate_on_submit():
        time = form.heure.data
        date2 = form.date.data
        if "name_server" in session:
            name_server1 = session["name_server"]

        admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
        admin_id = admin.id_user

        chosen_Server_RAM_information = database.sesh.query(database.Ram_Status).filter(
            and_(database.Server.id_owner.ilike(admin_id), database.Ram_Status.heure == time,
                database.Ram_Status.server_RAM == name_server1, database.Ram_Status.date == date2))
        for i in chosen_Server_RAM_information:
            memTotal.append(i.MemTotal)
            memFree.append(i.MemFree)
            memAvailable.append(i.MemAvailable)
            buffers.append(i.Buffers)
            cached.append(i.Cached)
            date1.append(i.date)
            heure1.append(i.heure)

    return render_template('datetimeRamf.html', form=form, memTotal=memTotal, memFree=memFree, memAvailable=memAvailable, buffers=buffers, cached=cached, date1=date1, heure1=heure1)




@app.route('/dashboard2', methods=['GET' , 'POST'])
@login_required
def dashboard2():
    current_user.username
    s_name = []
    s_ip = []
    s_id = []
    admin = database.sesh.query(database.User).filter(database.User.username.ilike(current_user.username)).first()
    admin_id = admin.id_user
    serveurs = database.sesh.query(database.Server).filter(database.Server.id_owner.ilike(admin_id)).all()
    for i in serveurs:
        s_name.append(i.name_server)
        s_ip.append(i.ip_address)
        s_id.append(i.id_server)

    return render_template('dashboard2.html', data1=s_name, data2=s_ip, data3=s_id, alpha=len(s_name), name=current_user.username)


@app.route('/plot_gr') #cette page permet l'affichage du graphe des quantités de mémoire occupée par les processus
@login_required
def plot_gr():
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

    def graphes_rss(device):
        device.send_command("/graph.sh --pie name -s rss")
        values = device.send_command(" cat /fich_value")
        labels = device.send_command(" cat /fich_labels")
        valeur = values.replace('[', '')
        valeur1 = valeur.replace(']', '')
        val1 = valeur1.split(',')

        labels1 = labels.replace('[', '')
        labels2 = labels1.replace('] ', '')
        lab1 = labels2.split(',')
        var = []

        for i in range(len(val1)):
            var.append(float(val1[i]))

        fig = pyplot.figure()
        axes = fig.add_subplot(111)
        axes.pie(var, labels=lab1, autopct="%.2f%%", startangle=90, shadow=True)
        axes.axis('equal')
        # axes.title("Graphe pie of Resident Set Size(RSS)")
        fig.tight_layout()
        return fig
    fig = graphes_rss(device)   #la variable device est la même que celle qui se trouve déja la partie flask et que tu as dû changer
    output = io.BytesIO()        #par une variable de session il suffit de la remplacer
    FigureCanvas(fig).print_png(output)  #  RSS = Resident Set Size (tu peux le mettre comme titre de ce graphe si tu veux)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/graphe_pss')       #cette page permet d'afficher le graphe de la portion de mémoire principale occupé par un processus
@login_required
def graphe_pss():   #et de la mémoire privée de ce processus
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

    def graphes_pss(device):
        device.send_command("/graph.sh --pie name -s pss")
        values = device.send_command(" cat /fich_value")
        labels = device.send_command(" cat /fich_labels")
        valeur = values.replace('[', '')
        valeur1 = valeur.replace(']', '')
        val1 = valeur1.split(',')

        labels1 = labels.replace('[', '')
        labels2 = labels1.replace('] ', '')
        lab1 = labels2.split(',')
        var = []

        for i in range(len(val1)):
            var.append(float(val1[i]))

        fig = pyplot.figure()
        axes = fig.add_subplot(111)
        axes.pie(var, labels=lab1, autopct="%.2f%%", startangle=90, shadow=True)
        axes.axis('equal')
        # axes.title("Graphe pie of Proportional Set Size(PSS)")
        fig.tight_layout()
        return fig
    fig = graphes_pss(device)   # PSS = Proportional Set Size (tu peux le mettre comme titre du graphe sur la page)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/changeAddress', methods=['GET' , 'POST'])
@login_required
def changeAddress():
    form = classes.changeAddress()
    data = ""
    if form.validate_on_submit():
        name_server = form.name_server.data
        ip_address = form.ip_address.data

        obj2 = database.sesh.query(database.Server).filter(database.Server.name_server.ilike(name_server)).all()
        if obj2 == None:
            data = "This name does not exist"
        else:
            data = "You IP Address has been changed successfully!"

        database.sesh.query(database.Server).filter(database.Server.name_server.ilike(name_server)).update({database.Server.ip_address: ip_address}, synchronize_session=False)
        database.sesh.commit()

    return render_template('changeAddress.html', form=form, data=data)

if __name__ == '__main__':
    app.run(debug=False)
