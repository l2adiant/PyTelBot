import logging
from telegram.ext import *
from telegram import *
from datetime import datetime
#import responses
import sqlite3
from tabulate import tabulate
from constant import ALLOWED_RSO, TELENOR_NUM, ALLOWED_ADMIN

import os
PORT = int(os.environ.get('PORT', '8443'))
TOKEN = os.environ.get('API_KEY')


conn = sqlite3.connect('FCA.db')
print ("Opened database successfully");


# API_KEY = ''
today = datetime.today()
TodayDate = today.strftime("%d/%m/%Y")
CurrentTime = today.strftime("%H:%M:%S")
ThisMonth = today.strftime("%m/%Y")



# Set up the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.info('Starting Bot...')

### Start Command ######################################################
def start_command(update: Update, context):
    update.message.reply_text(update.message.chat.first_name + ' \nWelcome to Telenor Franchise' + '\n\nyour username is: ' +  update.message.chat.username + '\nchat id is: ' + str(update.message.chat_id))

### RSO to Get Today's Sale ######################################################
def today_command(update, context):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username

    while True:
        answer = (username)
        if any(item == answer for item in ALLOWED_RSO):
            conn = sqlite3.connect('FCA.db')
            cursor = conn.cursor()
            sql = "SELECT COUNT (*) FROM tabb WHERE rso = ? AND date = ?"
            cursor.execute(sql,(username, TodayDate,))
            fcaCount = cursor.fetchone()[0]
            FcaCount_asstring = str(fcaCount)
            update.message.reply_text('Hey ' + first_name + '\nYour ' + ' ' + TodayDate + ' ' + 'sale is' + ' ' + FcaCount_asstring)
            print('Hey ' + first_name + ' Your ' + ' ' + TodayDate + ' ' + 'sale is' + ' ' + FcaCount_asstring)

            sql1 = "SELECT msisdn,time FROM tabb WHERE rso = ? AND date = ? ORDER BY id ASC"
            cursor.execute(sql1, (username, TodayDate,))

            results = cursor.fetchall()
            #print(results)
            print(tabulate(results, headers=["MSISDN", "Time"], tablefmt="presto"))
            update.message.reply_text(tabulate(results, headers=["MSISDN", "Time"], tablefmt="presto"))

            break
        update.message.reply_text('Admin can not perform this action')
        break

### RSO to Get Monthly Sale ######################################################
def monthly_command(update, context):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username

    while True:
        answer = (username)
        if any(item == answer for item in ALLOWED_RSO):
            conn = sqlite3.connect('FCA.db')
            cursor = conn.cursor()
            sql2 = "SELECT COUNT (*) FROM tabb WHERE rso = ? AND bymonth = ?"
            cursor.execute(sql2, (username, ThisMonth,))
            fcaCount = cursor.fetchone()[0]
            FcaCount_asstring = str(fcaCount)
            update.message.reply_text('Hey ' + first_name + '\nYour this month sale is' + ' ' + FcaCount_asstring)
            print('Hey ' + first_name + ' Your ' + ' ' + TodayDate + ' ' + 'sale is' + ' ' + FcaCount_asstring)

            sql3 = "SELECT msisdn,date FROM tabb WHERE rso = ? AND bymonth = ? ORDER BY id DESC"
            cursor.execute(sql3, (username, ThisMonth,))
            results = cursor.fetchall()
            #print(results)
            print(tabulate(results, headers=["MSISDN", "Date"],tablefmt="presto"))
            update.message.reply_text(tabulate(results, headers=["MSISDN", "Date"], tablefmt="presto"))

            break
        update.message.reply_text('Admin can not perform this action')
        break

### Help Command ######################################################
def help_command(update, context):
    update.message.reply_text('help commands')

### Admin Daily sale ######################################################
def admintoday_command(update, context):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username


    while True:
        answer = (username)
        if any(item == answer for item in ALLOWED_ADMIN):
            conn = sqlite3.connect('FCA.db')
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT (DISTINCT msisdn) From tabb WHERE date = '%s'" %TodayDate)
            AdminTodayFCASum = cursor.fetchone()[0]
            AdminTodayFCASumAsStr = str(AdminTodayFCASum)

            update.message.reply_text('FCA Dated ' + TodayDate + ' is ' + AdminTodayFCASumAsStr)
            cursor.execute("SELECT rso, COUNT(DISTINCT msisdn) FROM tabb WHERE date = '%s' GROUP BY rso ORDER BY COUNT(msisdn) DESC" %TodayDate)
            fcaCount = cursor.fetchall()
            #print(fcaCount)
            print(tabulate(fcaCount, headers=["RSO", "Qty"], tablefmt="presto"))
            update.message.reply_text(tabulate(fcaCount, headers=["RSO", "Qty"], tablefmt="presto"))

            break
        update.message.reply_text('You are not authorised, please contact administrator')
        break

### Admin Monthly sale report######################################################
def adminmonthly_command(update, context):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username


    while True:
        answer = (username)
        if any(item == answer for item in ALLOWED_ADMIN):
            conn = sqlite3.connect('FCA.db')
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT (DISTINCT msisdn) From tabb WHERE bymonth = '%s'" %ThisMonth)
            AdminTodayFCASum = cursor.fetchone()[0]
            AdminTodayFCASumAsStr = str(AdminTodayFCASum)

            update.message.reply_text('FCA Performed this month is ' + AdminTodayFCASumAsStr)
            cursor.execute("SELECT rso, COUNT(DISTINCT msisdn) FROM tabb WHERE bymonth = '%s' GROUP BY rso ORDER BY COUNT(msisdn) DESC" %ThisMonth)
            fcaCount = cursor.fetchall()
            #print(fcaCount)
            print(tabulate(fcaCount, headers=["RSO", "Qty"], tablefmt="presto"))
            update.message.reply_text(tabulate(fcaCount, headers=["RSO", "Qty"], tablefmt="presto"))

            break
        update.message.reply_text('You are not authorised, please contact administrator')
        break


###################################################################################
###################################################################################
###################################################################################
###################################################################################
###################################################################################

def get_response(input_text, context, update):
    user_message = str(input_text).lower()
    FCA_MESSAGE = user_message.split(" ")
    TelCode = FCA_MESSAGE[1][:3]
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    username = update.message.chat.username
####  fcax 3451234567 ##############
    while True:

        if str(FCA_MESSAGE[0]) == 'fcax':

            answer = TelCode
            if any(item == answer for item in TELENOR_NUM):
                print(answer)
            else:
                return answer + " is Not Telenor number"

            answer = username
            if any(item == answer for item in ALLOWED_RSO):
                print(answer)
            else:
                return "You are not Authorise to perform FCAX operation"

            if len(FCA_MESSAGE[1]) == 10:
                print('')
            else:
                return "Please recheck, number length should be 10"

            con = sqlite3.connect('FCA.db')
            cursor = con.cursor()

            # Create table
            try:
                cursor.execute('''CREATE TABLE IF NOT EXISTS tabb (id INTEGER PRIMARY KEY autoincrement, msisdn text unique, 
                                rso text, type text, date TEXT, time text, bymonth text)''')

            except:
                pass

            # Insert a row of data
            val = [FCA_MESSAGE[1], username, FCA_MESSAGE[0], TodayDate, CurrentTime, ThisMonth]
            try:
                cursor.execute("INSERT INTO tabb (msisdn, rso, type, date, time, bymonth) VALUES (?,?,?,?,?,?)",
                               val)
            except:
                return 'MSISDN ' + FCA_MESSAGE[1] + " Already exist"
                print("Enter differe value")
            ### Save (commit) the changes

            results = cursor.fetchone()
            print(results)
            con.commit()

            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.
            con.close()
            print(cursor.lastrowid)

            return FCA_MESSAGE[1] + " successfully added into database"

        break

    while True:

        if str(FCA_MESSAGE[0]) == 'fca':

            answer = TelCode
            if any(item == answer for item in TELENOR_NUM):
                print('TELENOR NUM OK')
            else:
                return answer + " is Not Telenor number"

            if str(FCA_MESSAGE[2]) == 'aasimpk':
                print('ID FOUND')
            else:

                con = sqlite3.connect('FCA.db')
                cursor = con.cursor()

                # Create table
                try:
                    cursor.execute('''CREATE TABLE IF NOT EXISTS tabb (id INTEGER PRIMARY KEY autoincrement, msisdn text unique, 
                    rso text, type text, date TEXT, time text, bymonth text)''')

                except:
                    pass

                # Insert a row of data
                val = [FCA_MESSAGE[1], FCA_MESSAGE[2], FCA_MESSAGE[0], TodayDate, CurrentTime,ThisMonth]
                try:
                    cursor.execute("INSERT INTO tabb (msisdn, rso, type, date, time, bymonth) VALUES (?,?,?,?,?,?)",
                                   val)
                except:
                    return 'MSISDN ' + FCA_MESSAGE[1] + " Already exist"
                    print("Enter differe value")
                ### Save (commit) the changes

                results = cursor.fetchone()
                print(results)
                con.commit()

                # We can also close the connection if we are done with it.
                # Just be sure any changes have been committed or they will be lost.
                con.close()
                print(cursor.lastrowid)

            return FCA_MESSAGE[1] + " successfully added into database"

        break

    while True:
        answer = username
        if any(item == answer for item in ALLOWED_RSO):
            print(answer)
        else:
            return "You are not Authorise to perform FCAX operation"

            if str(FCA_MESSAGE[0]) == 'get':
                print('')
            else:
                return "Use proper command Get Fca DD/MM/YYYY to get date wise FCA Report"

            if str(FCA_MESSAGE[1]) == 'fca':
                print('')

                conn = sqlite3.connect('FCA.db')
                cursor = conn.cursor()
                sql = "SELECT COUNT (*) FROM tabb WHERE rso = ? AND date = ?"
                cursor.execute(sql, (username, FCA_MESSAGE[2],))
                fcaCount = cursor.fetchone()[0]
                sql1 = "SELECT msisdn,date FROM tabb WHERE rso = ? AND date = ? ORDER BY id ASC"
                cursor.execute(sql1, (username, FCA_MESSAGE[2],))

                results = cursor.fetchall()
                # print(results)
                print(tabulate(results, headers=["MSISDN", "Date"], tablefmt="presto"))

                return "Total FCA is " + str(fcaCount) + "\n\n" + tabulate(results, headers=["MSISDN", "Date"], tablefmt="presto")

        break


    while True:

        if str(FCA_MESSAGE[0]) == 'verify':

            answer = TelCode
            if any(item == answer for item in TELENOR_NUM):
                print(answer)
            else:
                return answer + " is Not Telenor number"

            answer = username
            if any(item == answer for item in ALLOWED_RSO):
                print(answer)
            else:
                return "You are not Authorise to perform FCAX operation"

            if len(FCA_MESSAGE[1]) == 10:
                print('')
            else:
                return "Please recheck, number length should be 10"

            conn = sqlite3.connect('FCA.db')
            cursor = conn.cursor()

            sql = "SELECT rso, date, time, msisdn FROM tabb WHERE msisdn = ?"
            cursor.execute(sql, (FCA_MESSAGE[1],))

            results = cursor.fetchall()
            print(tabulate(results, headers=["RSO", "Date", "Time", "MSISDN"]))

            return "MSISDN Result" + "\n\n" + tabulate(results, headers=["RSO", "Date", "Time", "MSISDN"])

        break

    return "Use proper command or type /help"

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.effective_chat.send_message("update.message_message" + str(update.effective_chat.id))
    print('added')


def handle_message(update, context):
    text = str(update.message.text).lower()
    logging.info(f'User ({update.message.chat.id}) says: {text}')

    # Bot response
    response = get_response(text, context, update)
    #update.message.reply_text(response)
    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def error(update, context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')


# Run the programme
if __name__ == '__main__':
    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('today', today_command))
    dp.add_handler(CommandHandler('monthly', monthly_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('admintoday', admintoday_command))
    dp.add_handler(CommandHandler('adminmonthly', adminmonthly_command))

    # Messages
    filtertxt = '[fca]\s\d{7}$'
    #dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.regex(filtertxt) & ~Filters.command, echo))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))


    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    # updater.start_polling(1.0)
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url="https://telegram-bot-asim.herokuapp.com/" + TOKEN)
    updater.idle()
