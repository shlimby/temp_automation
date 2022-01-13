# libraries
import time
import telepot
import adafruit_dht
import board
import sqlite3
from telepot.loop import MessageLoop

# variables and initialization
temperature_c = 0
temperature_f = 0
humidity = 0

message = ""  # message from telegram
# connection only with the database (Datenbank) directly
conn = sqlite3.connect('./home_server/db.sqlite3')
# reading the data
# SELECT means, we read the data from database
cursor = conn.execute(
    "SELECT * from temp_app_chatuser where username = 'James'")

# data for the user (token, chatid, userid) for Telegram
for row in cursor:
    token = row[2]
    chatid = row[3]
    userid = row[0]

dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)  # sensor

# function which receives the message


def handle(msg):
    global message
    message = msg['text']


# we take the token and create the bot
bot = telepot.Bot(token)

bot.getMe()  # direct message
bot.getUpdates()  # group message

# loop, where we read all the messages
# we have two threads: one for receiving message, one for sending message
MessageLoop(bot, handle).run_as_thread()

send_go = False


while True:
    if not send_go:
        bot.sendMessage(chatid, "Type go to start")
        message = ""
        send_go = True
        time.sleep(1)

    # while message == "":
    #     try:
    #         temperature_c = dhtDevice.temperature
    #         temperature_f = temperature_c * (9 / 5) + 32
    #         humidity = dhtDevice.humidity
    #     except:
    #         time.sleep(1)
    #     time.sleep(1)

    if message == "exit":
        bot.sendMessage(chatid, "Now it is closed")
        break

    if message == "go":
        send_go = False

        # selecting location only for the user
        cursor = conn.execute(
            "SELECT a.* from temp_app_place a join temp_app_place_owner b on a.id = b.place_id where b.chatuser_id =" + str(userid))
        # first showing locations, then asking to select location
        empty = True
        for row in cursor:
            empty = False  # it is not empty => we have data
            s = str(row[0])
            s += ' '
            s += row[5]
            # print(s)
            bot.sendMessage(chatid, s)
        if empty:
            bot.sendMessage(chatid, 'No location found for the user')
            continue

        bot.sendMessage(chatid, 'Please select a location')
        message = ""

        while message == "":
            time.sleep(1)  # we check input every second

        # we are selecting the room in the location
        cursor = conn.execute(
            "SELECT * from temp_app_room where id ='" + message + "'")
        empty = True
        for row in cursor:
            empty = False
            s = str(row[0])
            s += ' '
            s += row[2]  # room name
            bot.sendMessage(chatid, s)

        if empty:
            bot.sendMessage(chatid, 'No room found in the location')
            continue

        bot.sendMessage(chatid, 'Please select a room')
        message = ""

        while message == "":
            time.sleep(1)

        # Get tmep od snensor
        cursor = conn.execute("SELECT * from temp_app_entrie where sensor_id ='" +
                              message + "' order by timestamp DESC LIMIT 1")

        out_id = -1
        for row in cursor:
            temperature_c = row[3]
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = row[4]
            s = " Temp: {:.1f} F / {:.1f} C    Humidity: {:.1f}% ".format(
                temperature_f, temperature_c, humidity)
            out_id = row[6]
            bot.sendMessage(chatid, s)

        if out_id != -1:
            cursor = conn.execute("SELECT * from temp_app_outsideentrie where id ='" +
                                  str(out_id) + "' order by timestamp DESC LIMIT 1")
            for row in cursor:
                temperature_c = row[2]
                temperature_f = temperature_c * (9 / 5) + 32
                humidity = row[3]
                s = s = " Outside: {:.1f} F / {:.1f} C    Humidity: {:.1f}% ".format(
                    temperature_f, temperature_c, humidity)
                bot.sendMessage(chatid, s)

    time.sleep(2)
