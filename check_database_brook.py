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
        self.warning_users_transfer = 600
        self.warning_vip_users_transfer = 3000

        self.default_baned_count=1
        self.default_baned_time=24
        self.max_baned_time=48

        self.transfers_users_data=[]
        self.vip_users = ['jarvis_sky', 'Aliafagh']
        self.ultimate_user = 'mortezaparsa'

        # Get All Baned Users
        self.baned_users = self.read_baned_users()

    def warning_message(self, username: str, calc: int):
        return f"سلام وقت بخیر @{username} \n هشدار بن اکانت : شما تا الان {calc} مگابایت مصرف کرده اید"

    def ban_message(self, username: str):
        return f"سلام وقت بخیر @{username} \n با عرض پوزش اکانت شما بن شد"

    def request_send_telegram_message(self, link: str):
        try:
            res = requests.get(link)
            if str(res) == "<Response [200]>":
                return True

            else:
                print(f"{cr.Fore.RED}{res}")
                return False

        except Error as e:
            print(f"{cr.Fore.RED}Error while sending Telegram Message", e)
            return False

    def send_telegram_message(self, message: str):
        link = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.reciver_id}&text={message}"
        counter = 0
        while counter <= 5:
            time.sleep(2)
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
        # Writing file
        with open('baned_users_list.txt', 'w') as openfile:
            # Writing from List
            for baned_user in self.baned_users:
                temp_user_info = baned_user.split(',')
                u = f"{temp_user_info[0]},{temp_user_info[1]}"
                openfile.write(u)

            openfile.close()

    def check_if_user_is_baned(self, username: str):
        # print(baned_users)
        for baned_user in self.baned_users:
            u = baned_user.split(',')[0]
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

    def save_transfers_users_data(self):
        transfers_users_list = json.dumps(self.transfers_users_data)
        with open("transfers_brook_list.json", "w") as outfile:
            outfile.write(transfers_users_list)
            outfile.close()
        
        print(f"{cr.Fore.GREEN}All Transfers Users Data Was Writed.")

    def set_ban_time_proccess(self,id:str , username:str):
        for data in self.transfers_users_data:
            if data['user']==username:
                if 'baned_count' in data.keys():
                    # Update Objects
                    baned_count=int(data['baned_count'])+1
                    # user_time=int(data['time'])+(baned_count*self.default_baned_time)
                    user_time=self.max_baned_time
                    objects={'baned_count':baned_count,'time':user_time}
                    data.update(objects)

                else:
                    # Set First Ban User Objects
                    objects={'baned_count':self.default_baned_count,'time':self.default_baned_time}
                    data.update(objects)
                
                break
        
        # Write In To File
        self.save_transfers_users_data()

    def ban_user(self, id: str, username: str, transfer: int):
        counter = 0
        while counter <= 5:
            time.sleep(1)
            result = self.request_ban_user(id)
            if result == True:
                # Set Ban Time Proccess
                self.set_ban_time_proccess(id,username)

                # Write Baned Users In Text File
                self.baned_users.append(f"{username},{transfer}\n")
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
                print(
                    f"{cr.Fore.RED}Error while connecting to Database For Getting Users", e)
                if connection.is_connected():
                    cursor.close()
                    connection.close()
                return False

    def read_transfer_users_data(self):
        with open('transfers_brook_list.json', 'r') as openfile:
            # Reading from json file
            json_objects = json.load(openfile)
            openfile.close()

        self.transfers_users_data = json_objects

    def proccess_data(self, get_users_result: list):
        for row in get_users_result:
            if row[1] != self.ultimate_user:
                for data in self.transfers_users_data:
                    if data['user'] == row[1]:
                        last_transfer = int(data['transfer'])
                        current_transfer = int(row[7])
                        calc = current_transfer-last_transfer

                        # print(f"username: {data['user']} transfer:{calc}")

                        if data['user'] in self.vip_users:
                            if calc > self.limit_vip_users_transfer:
                                # User Should Be Banne
                                s = f"user: {row[1]} transfer: {calc}"
                                print(
                                    f"{cr.Fore.RED}Max Transfer Found On {cr.Fore.CYAN}VIP {cr.Fore.YELLOW}{s}")

                                # Baning Acount
                                if not self.check_if_user_is_baned(username=row[1]):
                                    ban_result = self.ban_user(
                                        id=row[0], username=row[1], transfer=calc)
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
                                telegram_result = self.send_telegram_message(
                                    message=self.warning_message(username=row[1], calc=calc))
                                if not telegram_result:
                                    print(
                                        f"{cr.Fore.RED} Message Not Sended For {row[1]} User !!!!")

                        # print(f"user: {data['user']} calc : {calc}")
                        elif calc > self.limit_users_transfer:
                            # User Should Be Banne
                            s = f"user: {row[1]} transfer: {calc}"
                            print(
                                f"{cr.Fore.RED}Max Transfer Found On {cr.Fore.YELLOW}{s}")

                            # Baning Acount
                            if not self.check_if_user_is_baned(username=row[1]):
                                ban_result = self.ban_user(
                                    id=row[0], username=row[1], transfer=calc)
                                if ban_result:
                                    print(
                                        f"{cr.Fore.CYAN} User {row[1]} Successfuly Baned.")
                                else:
                                    print(
                                        f"{cr.Fore.RED} User {row[1]} Not Baned!!!")

                                # Sending Telegram Message
                                telegram_result = self.send_telegram_message(
                                    message=self.ban_message(username=row[1]))
                                if not telegram_result:
                                    print(
                                        f"{cr.Fore.RED} Message Not Sended For {row[1]} User !!!!")

                        elif calc > self.warning_users_transfer:
                            # Send Warning Message
                            s = f"user: {row[1]} transfer: {calc}"
                            print(
                                f"{cr.Fore.YELLOW}Warning for {cr.Fore.WHITE}{s}")

                            # Sending Telegram Message
                            telegram_result = self.send_telegram_message(
                                message=self.warning_message(username=row[1], calc=calc))
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
        bd.read_transfer_users_data()

        # Proccess Data
        bd.proccess_data(get_users_result)

        # Sending Seprator
        bd.send_telegram_message("-"*59)

    print(f"{cr.Fore.BLUE}-"*50)


# -------------------------------------------------------------------------------------------
schedule.every(15).minutes.do(start)

while True:
    schedule.run_pending()
    time.sleep(1)
