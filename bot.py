import re
import time
import telebot
import threading
import googleapi

from telebot import types
from datetime import datetime
from datetime import timedelta
from database import *
from messages import *

access_token = ''
bot = telebot.TeleBot(access_token)

commands = ['/start', '/stop']


def generateMenu(userID):
    button1 = types.KeyboardButton('Рестораны')
    button2 = types.KeyboardButton('Культурный отдых')
    button3 = types.KeyboardButton('Магазины')
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu.add(button1)
    menu.add(button2)
    menu.add(button3)
    bot.send_message(userID, m_button, reply_markup=menu)


def clock(interval):
    while True:
        for k, v in users.items():
            for j in v['works']:
                if (datetime.now() + timedelta(minutes=10)).time().strftime('%H:%M') == j['date'].strftime('%H:%M'):
                    bot.send_message(v['user'], m_reminder10(v['name'], j['description']))

                if datetime.now().time().strftime('%H:%M') == j['date'].strftime('%H:%M'):
                    bot.send_message(v['user'], m_reminder(j['description']))
                    deleteWorks(v['user'], j)
        time.sleep(interval)


def check():
    for k, v in users.items():
        string = ''
        for j in v['works']:
            if j['date'] < datetime.now():
                string = string + j['description'] + ' в ' + j['date'].strftime('%H:%M') + '\n'
                deleteWorks(v['user'], j)

        if string != '':
            bot.send_message(v['user'], m_ex(string))

        if v['geolocationState'] != 0:
            resetGeoLocationState(v['user'])
            bot.send_message(v['user'], m_geo)
            generateMenu(v['user'])


@bot.message_handler(regexp='^Рестораны|Культурный отдых|Магазины$')
def echo(messages):
    mesText = messages.text
    userID = messages.chat.id

    if mesText == 'Рестораны':
        sendGeoLocationState(userID, 1)
    elif mesText == 'Культурный отдых':
        sendGeoLocationState(userID, 2)
    elif mesText == 'Магазины':
        sendGeoLocationState(userID, 3)

    button = types.KeyboardButton('Отправить геопозиицю', request_location=True)
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu.add(button)

    bot.send_message(userID, m_sendGeo, reply_markup=menu)


@bot.message_handler(commands=['start'])
def echo(messages):
    userID = messages.chat.id

    if userID in users:
        bot.send_message(userID, m_userExist)
        return

    bot.send_message(userID, m_welcome1)


@bot.message_handler(commands=['stop'])
def echo(messages):
    userID = messages.chat.id
    if deleteUser(userID):
        bot.send_message(userID, m_goodBye, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(regexp='^напомни')
def echo(messages):

    userID = messages.chat.id

    p = re.compile('^напомни *([\wа-яА-Я][\wа-яА-Я ]+[\wа-яА-Я]) *в *(2[0-3]|[0-1]?\d:[0-5]\d)', re.IGNORECASE)

    if userID not in users:
        bot.send_message(userID, m_noAuth)
        return

    if not p.match(messages.text):
        bot.send_message(userID, m_commandNotFound)
        return

    parse = p.split(messages.text)

    com = parse[1]
    com = re.sub(r'\s+', ' ', com)
    date = datetime.strptime(str(datetime.today().date()) + ' ' + parse[2], '%Y-%m-%d %H:%M')

    if date < datetime.now():
        bot.send_message(userID, m_timePassed)
        return

    for i in users[userID]['works']:
        if date == i['date']:
            bot.send_message(userID, m_hasPlan)
            return

    addNewWorks(userID, {'description': com, 'date': date})

    bot.send_message(messages.chat.id, m_plan(date.strftime('%H:%M')))


@bot.message_handler(content_types=['text'])
def echo(messages):
    if messages.text in commands:
        return

    userID = messages.chat.id

    if addNewUser(userID, messages.text):
        bot.send_message(userID, m_welcome2(users[userID]['name']))
        generateMenu(userID)


@bot.message_handler(content_types=['location'])
def echo(message):
    location = message.location
    userID = message.chat.id

    location = {'lat': location.latitude, 'lng': location.longitude}
    places = googleapi.getplaces(location, users[userID]['geolocationState'])

    if len(places) != 0:
        bot.send_message(userID, m_foundPlace)

    chet = 0
    places = reversed(places)

    for i in places:
        if chet == 5:
            break
        bot.send_message(userID, i['name'])
        bot.send_location(userID, latitude=i['location']['lat'], longitude=i['location']['lng'])
        chet = chet + 1

    generateMenu(userID)

if __name__ == '__main__':
    recoveryData()
    check()

    t = threading.Thread(target=clock, args=(60,))
    t.daemon = True
    t.start()

    bot.polling(none_stop=True)