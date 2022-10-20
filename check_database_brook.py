from itertools import count
import json
import time
import requests
import schedule
import mysql.connector
import colorama as cr
from mysql.connector import Error

cr.init(autoreset=True)


class BrookData:
    def __init__(self):
        self.token = '5574072380:AAE9EwlaoM8bQcAK0Epexjo-mk2Iuugiswk'
        self.reciver_id = "-1001833835639"
        self.a_token = 'ca48cd29edf80e30a57a8d705172fc2a97cf5c60653b421046eafe30cebb9ad1f51227b7f7002e3dc5c756c71c7ff9c1a1103bf49fd34ed6'
        self.ban_url = "https://irvpn.co/adminapi/ban_user"

        self.limit_users_transfer = 1024
        self.limit_vip_users_transfer = 5120
        self.warning_users_transfer = 700
        self.warning_vip_users_transfer = 4000

        self.vip_users = ['jarvis_sky', 'Aliafagh']
        self.ultimate_user = 'mortezaparsa'

        # Get All Baned Users
        self.baned_users = self.read_baned_users()

    def warning_message(self,username:str,calc: int):
        return f"سلام وقت بخیر @{username} \n هشدار بن اکانت : شما تا الان {calc} مگابایت مصرف کرده اید"

    def ban_message(self,username:str):
        return f"سلام وقت بخیر @{username} \n با عرض پوزش اکانت شما بن شد"

    def request_send_telegram_message(self, link: str):
        try:
            res = requests.get(link)
            if str(res) == "<Response [200]>":
                return True

            else:
                # print(f"{cr.Fore.RED}{res}")
                return False

        except Error as e:
            print(f"{cr.Fore.RED}Error while sending Telegram Message", e)
            return False

    def send_telegram_message(self, message: str):
        link = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.reciver_id}&text={message}"
        counter = 0
        while counter <= 5:
            result = self.request_send_telegram_message(link=link)
            if result == True:
                return True

            counter = counter+1

        return False

    def read_baned_users(self):
        with open('baned_users_list.txt', 'r') as openfile:
            # Reading from json file
            baned_users_list = openfile.readlines()
            openfile.close()

        return baned_users_list

    def write_ban_user(self):
        with open('baned_users_list.txt', 'w') as openfile:
            # Writing from List
            for baned_user in self.baned_users:
                u = baned_user.split()[0]
                openfile.write(u)
                openfile.write("\n")

            openfile.close()

    def check_if_user_is_baned(self, username: str):
        # print(baned_users)
        for baned_user in self.baned_users:
            u = baned_user.split()[0]
            if u == username:
                return True

        return False

    def request_ban_user(self, id: str):
        try:
            post_data = {'id': id, 'token': self.a_token}

            res = requests.post(self.ban_url, json=post_data)
            if str(res) == "<Response [200]>":
                return True
            else:
                print(f"{cr.Fore.RED}{res}")
                return False
        except Error as e:
            print(f"{cr.Fore.RED}Error while Baning User", e)
            return False

    def ban_user(self, id: str, username: str):
        counter = 0
        while counter <= 5:
            result = self.request_ban_user(id)
            if result == True:
                self.baned_users.append(f"{username}\n")
                self.write_ban_user()
                return True

            counter = counter+1
        return False

    # def create_thread(id:str):
    #     threading.Thread(target=ban_user,args=(id)).start()

    def get_users(self):
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
                print(f"{cr.Fore.RED}Error while connecting to Database For Getting Users", e)
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                return False

    def read_transfer_users_data(self):
        with open('transfers_brook_list.json', 'r') as openfile:
            # Reading from json file
            json_objects = json.load(openfile)
            openfile.close()

        return json_objects

    def proccess_data(self, get_users_result: list, transfer_users_data: list):
        for row in get_users_result:
            if row[1] != self.ultimate_user:
                for data in transfer_users_data:
                    if data['user'] == row[1]:
                        last_transfer = int(data['transfer'])
                        current_transfer = int(row[7])
                        calc = current_transfer-last_transfer
                        for vip_user in self.vip_users:
                            if data['user'] == vip_user:
                                if calc > self.limit_vip_users_transfer:
                                    # User Should Be Banne
                                    s = f"user: {row[1]} transfer: {calc}"
                                    print(
                                        f"{cr.Fore.RED}Max Transfer Found On {cr.Fore.CYAN}VIP {cr.Fore.YELLOW}{s}")

                                    # Baning Acount
                                    if not self.check_if_user_is_baned(username=row[1]):
                                        ban_result = self.ban_user(
                                            id=row[0], username=row[1])
                                        if ban_result:
                                            print(
                                                f"{cr.Fore.CYAN} User {row[1]} Successfuly Baned.")
                                        else:
                                            print(
                                                f"{cr.Fore.RED} User {row[1]} Not Baned!!!")

                                        # Senging Message On Telegram
                                        telegram_result = self.send_telegram_message(
                                            message=self.ban_message(username=row[1]))
                                        if not telegram_result:
                                            print(
                                                f"{cr.Fore.RED} Message Not Sended For {row[1]} User !!!!")

                                elif calc > self.warning_vip_users_transfer:
                                    # Send Warning Message
                                    s = f"user: {row[1]} transfer: {calc}"
                                    print(
                                        f"{cr.Fore.YELLOW}Warning for {cr.Fore.CYAN}VIP {cr.Fore.WHITE}{s}")

                                    # Sending Telegram Message
                                    telegram_result = self.send_telegram_message(message=self.warning_message(username=row[1],calc=calc))
                                    if not telegram_result:
                                        print(
                                            f"{cr.Fore.RED} Message Not Sended For {row[1]} User !!!!")

                                # exit from loop after user doesn't touch limit
                                break
                        # print(f"user: {data['user']} calc : {calc}")
                        if calc > self.limit_users_transfer:
                            # User Should Be Banne
                            s = f"user: {row[1]} transfer: {calc}"
                            print(
                                f"{cr.Fore.RED}Max Transfer Found On {cr.Fore.YELLOW}{s}")

                            # Baning Acount
                            if not self.check_if_user_is_baned(username=row[1]):
                                ban_result = self.ban_user(
                                    id=row[0], username=row[1])
                                if ban_result:
                                    print(
                                        f"{cr.Fore.CYAN} User {row[1]} Successfuly Baned.")
                                else:
                                    print(
                                        f"{cr.Fore.RED} User {row[1]} Not Baned!!!")

                                # Sending Telegram Message
                                telegram_result = self.send_telegram_message(message=self.ban_message(username=row[1]))
                                if not telegram_result:
                                    print(
                                        f"{cr.Fore.RED} Message Not Sended For {row[1]} User !!!!")

                        elif calc > self.warning_users_transfer:
                            # Send Warning Message
                            s = f"user: {row[1]} transfer: {calc}"
                            print(
                                f"{cr.Fore.YELLOW}Warning for {cr.Fore.WHITE}{s}")

                            # Sending Telegram Message
                            telegram_result = self.send_telegram_message(message=self.warning_message(username=row[1],calc=calc))
                            if not telegram_result:
                                print(
                                    f"{cr.Fore.RED} Message Not Sended For {row[1]} User !!!!")

                        # exit from loop after user doesn't touch limit
                        break


# -------------------------------------------------------------------------------------------
def start():
    bd = BrookData()
    get_users_result = bd.get_users()

    if get_users_result is False:
        print(f"{cr.Fore.RED}Users Info Was Not Downloaded!!!")
        exit()

    else:
        # Get All Old Transfer Users Data
        transfer_users_data = bd.read_transfer_users_data()

        # Proccess Data
        bd.proccess_data(get_users_result, transfer_users_data)
        
        # Sending Seprator
        bd.send_telegram_message("-"*59)

    print(f"{cr.Fore.BLUE}-"*50)


# -------------------------------------------------------------------------------------------
schedule.every(15).minutes.do(start)

while True:
    schedule.run_pending()
    time.sleep(1)
