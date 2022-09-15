from netmiko import *
import database
from datetime import date, datetime
from netmiko import *
import threading
import database



def planification(device):
    device.find_prompt()

    scp_conn = SCPConn(device)
    scp_conn.scp_transfer_file(source_file="script.sh", dest_file="/")

    device.send_command("chmod 700/script.sh")
    device.send_command("sed -i 's/\\r$//' /script.sh")
    device.send_command(" echo 0-59/5 0-23 1-31 1-12 1-7  root  /script.sh >> /etc/crontab ")
    scp_conn.scp_transfer_file(source_file="graph.sh", dest_file="/")

    device.send_command("chmod 777 /graph.sh")
    device.send_command("sed -i 's/\\r$//' /graph.sh")


#the function that create user in server
def create_user(nom, mot_de_passe, device):
    device.find_prompt()
    output = device.send_command("useradd  %s" % nom)
    output1 = device.send_command("echo %s | passwd %s --stdin" % (nom, mot_de_passe))
    return (output, output1)

# the function that delete a user from server
def delete_user(nom, device):
    device.find_prompt()
    output = device.send_command("userdel %s" % nom)
    return (output)

#cette partie contient des fonctions qui permettent le remplissage des différentes tables


class Remplir(threading.Thread):     #classe définissant un thread pour remplir permanement la table d'état de la méroire
    def __init__(self, device, nom_serv):
        threading.Thread.__init__(self)
        self.device = device
        self.nom = nom_serv
        self._stopevent = threading.Event()
    def run(self):
        while not self._stopevent.isSet():
            self.device.find_prompt()
            output = self.device.send_command("cat /file_serv_1")
            output1 = self.device.send_command("cat /file_serv_2 ")
            f = output
            f1 = output1
            l = f.replace('\n', ',')
            l1 = f1.replace('   ', ',')
            b = l.split(',')
            b1 = l1.split(',')
            for i in range(len(b) - 1):
                b[i].rstrip('\n')

            for i in range(len(b1) - 1):
                b1[i].rstrip('\n')

            d = date.today().isoformat()
            now = datetime.now()
            h = now.strftime("%H:%M:%S")
            info = database.Ram_Status(MemTotal=b[0], MemFree=b[1], MemAvailable=b[2], Buffers=b[3], Cached=b[4],
                                       date=d, heure=h, server_RAM=self.nom)
            info1 = database.CPU_Status(user=b1[0], nice=b1[1], systeme=b1[2], iowait=b1[3], steal=b1[4], idele=b1[5],
                                        date1=d, heure1=h, server_CPU=self.nom)

            database.sesh.add(info)
            database.sesh.add(info1)
            database.sesh.commit()
            self._stopevent.wait(300.0)

    def stop(self):
        self._stopevent.set()

class Remplir2(threading.Thread):
    def __init__(self, device, nom_serv):
        threading.Thread.__init__(self)
        self.device = device
        self.nom = nom_serv
        self._stopevent = threading.Event()
    def run(self):
        while not self._stopevent.isSet():
            self.device.find_prompt()
            var = datetime.now().time()
            var = str(var)
            var1 = var[:5]
            if str(var1) in ["9:30", "12:30", "18:30"]:
                output1 = self.device.send_command("df -h | awk {'print $1'}")
                output2 = self.device.send_command("df -h | awk {'print $2'}")
                output3 = self.device.send_command("df -h | awk {'print $3'}")
                output4 = self.device.send_command("df -h | awk {'print $4'}")
                output5 = self.device.send_command("df -h | awk {'print $5'}")
                output6 = self.device.send_command("df -h | awk {'print $6'}")
                f2 = output1
                f3 = output2
                f4 = output3
                f5 = output4
                f6 = output5
                f7 = output6
                l2 = f2.replace('\n', ',')
                l3 = f3.replace('\n', ',')
                l4 = f4.replace('\n', ',')
                l5 = f5.replace('\n', ',')
                l6 = f6.replace('\n', ',')
                l7 = f7.replace('\n', ',')
                b2 = l2.split(',')
                b3 = l3.split(',')
                b4 = l4.split(',')
                b5 = l5.split(',')
                b6 = l6.split(',')
                b7 = l7.split(',')
                for i in range(len(b2) - 1):
                    da = date.today().isoformat()
                    he = datetime.now()
                    b2[i].rstrip('\n')
                    b3[i].rstrip('\n')
                    b4[i].rstrip('\n')
                    b5[i].rstrip('\n')
                    b6[i].rstrip('\n')
                    b7[i].rstrip('\n')
                    info2 = database.disc_Status(filesystem=b2[i + 1], size=b3[i + 1], used=b4[i + 1], avail=b5[i + 1],
                                      use_percent=b6[i + 1], mount_on=b7[i + 1], server_disc=self.nom, date2=da, heure2=str(he))
                    database.sesh.add(info2)
                    database.sesh.commit()
            self._stopevent.wait(2.0)
    def stop(self):
        self._stopevent.set()


class Remplir3(threading.Thread):
    def __init__(self, device, nom_serv):
        threading.Thread.__init__(self)
        self.device = device
        self.nom = nom_serv
        self._stopevent = threading.Event()
    def run(self):
        while not self._stopevent.isSet():
            self.device.find_prompt()
            output = self.device.send_command(" who | awk {'print $1'} ")
            output1 = self.device.send_command("who | awk {'print $3'}")
            output2 = self.device.send_command("who | awk {'print $4'}")
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

            for i in range(len(xb)):
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
                    ob = database.USERS(login=xb[i], date=xb1[i], temp=xb2[i], server_user=self.nom)
                    database.sesh.add(ob)
                    database.sesh.commit()
    def stop(self):
        self._stopevent.set()

def thread_fonc(device, nom_server):
    thread1 = Remplir(device, nom_server)
    thread2 = Remplir2(device, nom_server)
    thread1.start()
    thread2.start()

def affiche_user(device, nom_server):
    thread3 = Remplir3(device, nom_server)
    thread3.stop()
