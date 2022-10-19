import json
import time
import telepot
import requests
import schedule
import threading
from lib2to3.pgen2 import token
import mysql.connector
import colorama as cr
from mysql.connector import Error

cr.init(autoreset=True)

token = '5677357335:AAGauZANKo0qIspAMXJIPLqUixlrqYuhZ9Y'
a_token = 'ca48cd29edf80e30a57a8d705172fc2a97cf5c60653b421046eafe30cebb9ad1f51227b7f7002e3dc5c756c71c7ff9c1a1103bf49fd34ed6'
ban_url = "https://irvpn.co/adminapi/ban_user"
ban_message = "سلام وقت بخیر \n با عرض پوزش اکانت شما بن شد"

limit_users_transfer = 1024
limit_vip_users_transfer = 5120
warning_users_transfer = 700
warning_vip_users_transfer = 4000

baned_users=[]
vip_users = ['jarvis_sky', 'Aliafagh']
ultimate_user = 'mortezaparsa'


def warning_message(calc: int):
    return f"سلام وقت بخیر \n هشدار بن اکانت : شما تا الان {calc} مگابایت مصرف کرده اید"


def send_telegram_message(reciver_id: str, message: str):
    bot = telepot.Bot(token)
    bot.sendMessage(reciver_id, message)

def read_baned_users():
    with open('baned_users_list.json', 'r') as openfile:
        # Reading from json file
        print(f"read baned : {type(openfile)}")
        json_objects = json.load(openfile)
        openfile.close()

    return json_objects

def write_ban_user():
    json_objects = json.dumps(baned_users)
    with open('baned_users_list.json', 'w') as openfile:
        # Writing from List
        print(f"write baned : {type(json_objects)}")
        openfile.write(json_objects)
        openfile.close()

def check_if_user_is_baned(username:str):
    for user in baned_users:
        if user==username:
            return True
        
    return False

def request_ban_user(id: str):
    try:
        post_data = {'id': id, 'token': a_token}

        res = requests.post(ban_url, json=post_data)
        if str(res) == "<Response [200]>":
            return True
        else:
            print(f"{cr.Fore.RED}{res}")
            return False
    except Error as e:
        print(f"{cr.Fore.RED}Error while connecting to MySQL", e)
        return False


def ban_user(id: str,username:str):
    counter = 0
    while counter <= 5:
        result = request_ban_user(id)
        if result == True:
            baned_users.append(username)
            write_ban_user()
            return True

        counter = counter+1
    return False


# def create_thread(id:str):
#     threading.Thread(target=ban_user,args=(id)).start()


def get_users():
    counter = 0
    while counter <= 5:
        try:
            connection = mysql.connector.connect(host='198.244.140.109',
                                                 database='brook',
                                                 user='jarvis',
                                                 password='MH75d$4s#d9.f6bF')
            if connection.is_connected():
                cursor = connection.cursor()
                query = "SELECT * FROM user"
                cursor.execute(query)
                res = cursor.fetchall()
                return res
            else:
                return False

        except Error as e:
            print(f"{cr.Fore.RED}Error while connecting to MySQL", e)
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
            return False


def read_transfer_users_data():
    with open('transfers_brook_list.json', 'r') as openfile:
        # Reading from json file
        json_objects = json.load(openfile)
        openfile.close()

    return json_objects


def proccess_data(get_users_result: list, transfer_users_data: list):
    for row in get_users_result:
        if row[1] != ultimate_user:
            for data in transfer_users_data:
                if data['user'] == row[1]:
                    last_transfer = int(data['transfer'])
                    current_transfer = int(row[7])
                    calc = current_transfer-last_transfer
                    for vip_user in vip_users:
                        if data['user'] == vip_user:
                            if calc > limit_vip_users_transfer:
                                # User Should Be Banne
                                s = f"user: {row[1]} transfer: {calc}"
                                print(
                                    f"{cr.Fore.RED}Max Transfer Found On {cr.Fore.CYAN}VIP {cr.Fore.YELLOW}{s}")

                                # Baning Acount
                                if not check_if_user_is_baned(row[1]):
                                    ban_result = ban_user(row[0],row[1])
                                    if ban_result:
                                        print(
                                            f"{cr.Fore.CYAN} User {row[1]} Successfuly Baned.")
                                    else:
                                        print(
                                            f"{cr.Fore.RED} User {row[1]} Not Baned!!!")

                                    # Senging Message On Telegram
                                    if "id_telegram" in data:
                                        send_telegram_message(
                                            data['id_telegram'], ban_message)
                                    else:
                                        print(
                                            f"{cr.Fore.MAGENTA}ID Is Not Exitst For {cr.Fore.CYAN}{data['user']} {cr.Fore.MAGENTA}And Message Not Sent!")

                            elif calc > warning_vip_users_transfer:
                                # Send Warning Message
                                s = f"user: {row[1]} transfer: {calc}"
                                print(
                                    f"{cr.Fore.YELLOW}Warning for {cr.Fore.CYAN}VIP {cr.Fore.WHITE}{s}")

                                # Sending Telegram Message
                                if "id_telegram" in data:
                                    send_telegram_message(
                                        data['id_telegram'], warning_message(calc))
                                else:
                                    print(
                                        f"{cr.Fore.MAGENTA}ID Is Not Exitst For {cr.Fore.CYAN}{data['user']} {cr.Fore.MAGENTA}And Message Not Sent!")

                            # exit from loop after user doesn't touch limit
                            break
                    # print(f"user: {data['user']} calc : {calc}")
                    if calc > limit_users_transfer:
                        # User Should Be Banne
                        s = f"user: {row[1]} transfer: {calc}"
                        print(
                            f"{cr.Fore.RED}Max Transfer Found On {cr.Fore.YELLOW}{s}")

                        # Baning Acount
                        if not check_if_user_is_baned(row[1]):
                            ban_result = ban_user(row[0],row[1])
                            if ban_result:
                                print(
                                    f"{cr.Fore.CYAN} User {row[1]} Successfuly Baned.")
                            else:
                                print(f"{cr.Fore.RED} User {row[1]} Not Baned!!!")

                            # Sending Telegram Message
                            if "id_telegram" in data:
                                send_telegram_message(
                                    data['id_telegram'], ban_message)
                            else:
                                print(
                                    f"{cr.Fore.MAGENTA}ID Is Not Exitst For {cr.Fore.CYAN}{data['user']} {cr.Fore.MAGENTA}And Message Not Sent!")

                    elif calc > warning_users_transfer:
                        # Send Warning Message
                        s = f"user: {row[1]} transfer: {calc}"
                        print(f"{cr.Fore.YELLOW}Warning for {cr.Fore.WHITE}{s}")

                        # Sending Telegram Message
                        if "id_telegram" in data:
                            send_telegram_message(
                                data['id_telegram'], warning_message(calc))
                        else:
                            print(
                                f"{cr.Fore.MAGENTA}ID Is Not Exitst For {cr.Fore.CYAN}{data['user']} {cr.Fore.MAGENTA}And Message Not Sent!")

                    # exit from loop after user doesn't touch limit
                    break


def check_brook_database():

    get_users_result = get_users()

    if get_users_result is False:
        print(f"{cr.Fore.RED}Users Info Was Not Downloaded!!!")
        exit()

    else:
        # Get All Old Transfer Users Data
        transfer_users_data = read_transfer_users_data()

        # Get All Baned Users
        baned_users=read_baned_users()

        # Proccess Data
        proccess_data(get_users_result, transfer_users_data)

#-------------------------------------------------------------------------------------------
# schedule.every(1).minutes.do(check_brook_database)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

check_brook_database()
