from models import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///Data.db")
Base.metadata.create_all(bind=engine)
session = sessionmaker(bind=engine)

users = {}


def addNewUser(userID, name):
    global users
    if userID in users:
        return False

    users[userID] = {'user': userID, 'name': name, 'works': [], 'geolocationState': 0}
    s = session()

    s.add(Users(userID=userID, name=name, geolocationState=0))

    s.commit()
    s.close()

    return True


def sendGeoLocationState(userID, state):
    global users
    if userID not in users:
        return False

    if users[userID]['geolocationState'] == state:
        return False

    users[userID]['geolocationState'] = state

    s = session()

    s.query(Users).filter(Users.userID == userID).update({'geolocationState': state})

    s.commit()
    s.close()

    return True


def resetGeoLocationState(userID):
    return sendGeoLocationState(userID, 0)


def addNewWorks(userID, work):
    global users
    if userID not in users:
        return False

    users[userID]['works'].append(work)

    s = session()

    u = s.query(Users).filter(Users.userID == userID).first()
    s.add(Works(description=work['description'], date=work['date'], users=u))

    s.commit()
    s.close()

    return True


def recoveryData():
    global users
    s = session()

    for i in s.query(Users).all():
        users[i.userID] = {'user': i.userID, 'name': i.name, 'works': [], 'geolocationState': i.geolocationState}
        for j in s.query(Works).filter(Works.userID == i.userID).all():
            users[i.userID]['works'].append({'description': j.description, 'date': j.date})

    s.close()


def deleteWorks(userID, work):
    global users
    if userID not in users:
        return False

    users[userID]['works'].remove(work)

    s = session()

    s.query(Works).filter(Works.userID == userID).filter(Works.date == work['date']).delete()

    s.commit()
    s.close()

    return True


def deleteUser(userID):
    global users
    if userID not in users:
        return False

    del users[userID]

    s = session()

    u = s.query(Users).filter(Users.userID == userID).first()

    s.delete(u)

    s.commit()
    s.close()

    return True