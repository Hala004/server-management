from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date, Time
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

#engine = create_engine('mysql+pymysql://root@localhost:3306/test2')
engine = create_engine('mysql+mysqlconnector://root@127.0.0.1:3306/projet')

Base = declarative_base()
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
sesh = Session()

#At the first connection to the application, the user should create an account, so that he can then use our app to manage his servers.
class User(UserMixin, Base):
    __tablename__ = 'User'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(15), unique=True)
    password = Column(String(80))

    def get_id(self):
        return (self.id_user)


class Server(Base):
    __tablename__ = 'Server'
    id_server = Column(Integer, primary_key=True, autoincrement=True)
    id_owner = Column(Integer, ForeignKey('User.id_user'))
    name_server = Column(String(200))
    ip_address = Column(String(50))

    def __init__(self, name_server, ip_address):
        self.name_server = name_server
        self.ip_address = ip_address

    def __repr__(self):
        return "%s, \t%s" % (self.name_server, self.ip_address)


class Ram_Status(Base):
    __tablename__ = 'mem_ram'
    id_RAM = Column(Integer, primary_key=True, autoincrement=True)
    server_RAM = Column(String(50), ForeignKey('Server.name_server'))
    MemTotal = Column(String(50))
    MemFree = Column(String(50))
    MemAvailable = Column(String(50))
    Buffers = Column(String(50))
    Cached = Column(String(50))
    date = Column(String(15))
    heure = Column(Time)

    def __repr__(self):
        return "MemTotal= %s, \tMemFree = %s, \tMemAvailable= %s, \tBuffers= %s, \tCached= %s, \t%s, \t%s " % (self.MemTotal, self.MemFree, self.MemAvailable, self.Buffers, self.Cached, self.date, self.heure)

class CPU_Status(Base):
    __tablename__ = 'etat_cpu'
    id_CPU = Column(Integer, primary_key=True, autoincrement=True)
    server_CPU = Column(String(50), ForeignKey('Server.name_server'))
    user = Column(String(20))
    nice = Column(String(20))
    systeme = Column(String(20))
    iowait = Column(String(20))
    steal = Column(String(100))
    idele = Column(String(20))
    date1 = Column(String(20))
    heure1 = Column(String(30))

    def __repr__(self):
        return "user= %s \tnice= %s \tsysteme= %s \tiowait= %s \tsteal= %s \tidele= %s, \t%s, \t%s" % (self.user, self.nice, self.systeme,  self.iowait, self.steal, self.idele, self.date1, self.heure1)


class disc_Status(Base):
    __tablename__ = 'disc_dur'

    id_disc = Column(Integer, primary_key=True, autoincrement=True)
    server_disc = Column(String(50), ForeignKey('Server.name_server'))
    filesystem = Column(String(50))
    size = Column(String(20))
    used = Column(String(20))
    avail = Column(String(20))
    use_percent = Column(String(20))
    mount_on = Column(String(50))
    date2 = Column(String(20))
    heure2 = Column(String(30))

    def __repr__(self):
        return "%s  \t %s \t %s \t%s   \t %s \t%s, \t%s, \t%s" % (self.filesystem, self.size, self.used, self.avail, self.use_percent, self.mount_on, self.date2, self.heure2)


class USERS(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    server_user = Column(String(50), ForeignKey('Server.name_server'))
    login = Column(String(50))
    date = Column(String(20))
    temp = Column(String(20))

    def __repr__(self):
        return "%s, \t%s, \t%s" % (self.login, self.date, self.temp)





