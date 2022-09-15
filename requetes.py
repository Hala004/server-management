import database
import functions
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import and_


#lorsque l'utilisateur selectionne un serveur, la variable chosen_server va contenir le nom de ce serveur, et on affiche plusieurs bouttons:
# ->By date  ->By time  ->By date time   ->Real time
#il choisit un, et la variable user_choice va contenir la valeur de ce boutton
#date=variable contenant la date saisi par l'utilisateur.
#time=variable contenant l'heure saisi par l'utilisateur.
###########################################################################################################################################################



def show_RAM_Status(chosen_server, user_choice, date, time):
        if user_choice == "1":
            for MemTotal, MemFree, MemAvailable, Buffers, Cached, date, heure in database.sesh.query(database.Ram_Status).filter(
                    and_(database.Ram_Status.server_RAM == chosen_server,
                         database.Ram_Status.date == date)):
                print("MemTotal: {0}, MemFree: {1}, MemAvailable:{2}, Buffers:{3}, Cached:{4}, date:{5}, heure:{6}".format(
                         MemTotal, MemFree, MemAvailable, Buffers, Cached, date, heure))
        elif user_choice== "2":
            for MemTotal, MemFree, MemAvailable, Buffers, Cached, date , heure in database.sesh.query(database.Ram_Status).filter(
                    and_(database.Ram_Status.server_RAM == chosen_server,
                         database.Ram_Status.heure == time)):
                print("MemTotal: {0}, MemFree: {1}, MemAvailable:{2}, Buffers:{3}, Cached:{4}, date:{5}, heure:{6}".format(MemTotal, MemFree, MemAvailable, Buffers, Cached, date, heure))

        elif user_choice=="3":
            for MemTotal, MemFree, MemAvailable, Buffers, Cached, date, heure in database.sesh.query(database.Ram_Status).filter(
                    and_(database.Ram_Status.server_RAM == chosen_server,
                         database.Ram_Status.date == date,
                         database.Ram_Status.heure == time)):
                print("MemTotal: {0}, MemFree: {1}, MemAvailable:{2}, Buffers:{3}, Cached:{4}, date:{5}, heure:{6}".format(MemTotal, MemFree, MemAvailable, Buffers, Cached, date, heure))

        #else:#real time
            #for MemTotal, MemFree, MemAvailable, Buffers, Cached , date, heure in database.sesh.query(database.Ram_Status).filter(
                   # and_(database.Ram_Status.server_RAM == chosen_server,
                        # database.Ram_Status.date == max(database.Ram_Status.date),
                        # database.Ram_Status.heure == max(database.Ram_Status.heure))):
                #print("MemTotal: {0}, MemFree: {1}, MemAvailable:{2}, Buffers:{3}, Cached:{4}, date:{5}, heure:{6}".format(
                       # MemTotal, MemFree, MemAvailable, Buffers, Cached, date, heure))

################################################################################################################################################################
def show_CPU_Status(chosen_server,user_choice,date,time):
    if user_choice == "1":
        for user, nice, systeme, iowait, steal, idele,date1, heure1 in database.sesh.query(database.CPU_Status).filter(
                and_(database.CPU_Status.server_CPU == chosen_server,
                     database.CPU_Status.date1 == date)):

             print("user: {0}, nice: {1}, systeme:{2}, iowait:{3}, steal:{4}, idele:{5}, date:{6} , time: {7}".format(
                    user, nice, systeme, iowait, steal, idele,date1, heure1))
    elif user_choice == "2":
        for user, nice, systeme, iowait, steal, idele, date1, heure1 in database.sesh.query(database.CPU_Status).filter(
                and_(database.CPU_Status.server_CPU == chosen_server,
                     database.CPU_Status.heure1 == time)):

            print("user: {0}, nice: {1}, systeme:{2}, iowait:{3}, steal:{4}, idele:{5}, date:{6} , time: {7}".format(
                    user, nice, systeme, iowait, steal, idele, date1, heure1))

    elif user_choice == "3":
        for user, nice, systeme, iowait, steal, idele, date1, heure1 in database.sesh.query(database.CPU_Status).filter(
                and_(database.CPU_Status.server_CPU == chosen_server,
                     database.Ram_Status.date1 == date,
                     database.Ram_Status.heure1 == time)):

             print("user: {0}, nice: {1}, systeme:{2}, iowait:{3}, steal:{4}, idele:{5}, date:{6} , time: {7}".format(
                    user, nice, systeme, iowait, steal, idele, date1, heure1))

    #else:  # real time
        #for user, nice, systeme, iowait, steal, idele, date1, heure1 in database.sesh.query(database.CPU_Status).filter(
                #and_(database.CPU_Status.server_CPU == chosen_server,
                     #database.CPU_Status.date1 == max(database.CPU_Status.date1),
                     #database.CPU_Status.heure1 == max(database.CPU_Status.heure1))):

             #print("user: {0}, nice: {1}, systeme:{2}, iowait:{3}, steal:{4}, idele:{5}, date:{6} , time: {7}".format(
                    #user, nice, systeme, iowait, steal, idele, date1, heure1))

###########################################################################################################################################################
def show_disc_Status(chosen_server,user_choice,date,time):
    if user_choice == "1":
        for filesystem, size, used, avail, use_percent, mount_on, date2, heure2 in database.sesh.query(database.disc_Status).filter(
                and_(database.disc_Status.server_disc == chosen_server,
                database.disc_Status.date2 == date)):

                print("filesystem: {0}, size: {1}, used:{2}, avail:{3}, use_percent:{4}, mount_on:{5}, date:{6} , time: {7}".format(
                    filesystem, size, used, avail, use_percent, mount_on, date2, heure2))
    elif user_choice == "2":
        for filesystem, size, used, avail, use_percent, mount_on, date2, heure2 in database.sesh.query(
                database.disc_Status).filter(
                and_(database.disc_Status.server_disc == chosen_server,
                database.disc_Status.heure2 == time)):

                print("filesystem: {0}, size: {1}, used:{2}, avail:{3}, use_percent:{4}, mount_on:{5}, date:{6} , time: {7}".format(
                    filesystem, size, used, avail, use_percent, mount_on, date2, heure2))

    elif user_choice == "3":
        for filesystem, size, used, avail, use_percent, mount_on, date2, heure2 in database.sesh.query(
                database.disc_Status).filter(
                and_(database.disc_Status.server_disc == chosen_server,
                database.disc_Status.date2 == date,
                database.disc_Status.heure2 == time)):

            print("filesystem: {0}, size: {1}, used:{2}, avail:{3}, use_percent:{4}, mount_on:{5}, date:{6} , time: {7}".format(
                    filesystem, size, used, avail, use_percent, mount_on, date2, heure2))

    #else:  # real time
        #for filesystem, size, used, avail, use_percent, mount_on, date2, heure2 in database.sesh.query(
                #database.disc_Status).filter(
            #and_(database.disc_Status.server_disc == chosen_server,
                 #database.disc_Status.date2 == max(database.disc_Status.date2),
                 #database.disc_Status.heure2 == max(database.disc_Status.heure2))):

            #print("filesystem: {0}, size: {1}, used:{2}, avail:{3}, use_percent:{4}, mount_on:{5}, date:{6} , time: {7}".format(
                    #filesystem, size, used, avail, use_percent, mount_on, date2, heure2))

########################################################################################################################################
def show_Server_information(chosen_server):
    for name_server,ip_address in database.sesh.query(database.Server).filter(and_(chosen_server == database.Server.name_server)):
        print("server name: {0} , server ip address : {1}".format(name_server,ip_address))
#########################################################################################################################################

def show_SERVER_Users(chosen_server,user_choice,date,time):#pour afficher les utilisateurs connectes
    if user_choice == "1":
        for login, date, temp in database.sesh.query(database.USERS).filter(
                and_(database.USERS.server_name_user == chosen_server,
                     database.USERS.date == date)):
            print("login: {0}, date: {1}, temp:{2}".format(login,date, temp))
    elif user_choice == "2":
        for login, date, temp in database.sesh.query(database.USERS).filter(
                and_(database.USERS.server_name_user == chosen_server,
                     database.USERS.temp == time)):
            print("login: {0}, date: {1}, temp:{2}".format(login, date, temp))

    elif user_choice == "3":
        for login, date, temp in database.sesh.query(database.USERS).filter(
                and_(database.USERS.server_name_user == chosen_server,
                     database.USERS.date == date,
                     database.USERS.temp == time)):
            print("login: {0}, date: {1}, temp:{2}".format(login, date, temp))

    #else:  # real time
        #for login, date, temp in database.sesh.query(database.USERS).filter(
                #and_(database.USERS.server_name_user == chosen_server,
                     #database.USERS.date == max(database.USERS.date),
                     #database.USERS.temp == max(database.USERS.temp))):
            #print("login: {0}, date: {1}, temp:{2}".format(login, date, temp))

###########################################################################################################################################