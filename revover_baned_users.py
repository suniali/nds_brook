from importlib.util import set_loader
import json
import time
import requests
import schedule
import colorama as cr

cr.init(autoreset=True)

class RecoveryBanedUsers:

    def __init__(self) ->None:
        self.admin_telegram_id="@jarvis_sky"
        self.token = '5574072380:AAE9EwlaoM8bQcAK0Epexjo-mk2Iuugiswk'
        self.reciver_id = "-1001833835639"
        self.a_token = 'ca48cd29edf80e30a57a8d705172fc2a97cf5c60653b421046eafe30cebb9ad1f51227b7f7002e3dc5c756c71c7ff9c1a1103bf49fd34ed6'
        self.recover_url="https://irvpn.co/adminapi/recover_user"

        self.transfers_users_data=[]

    def recoverd_baned_user_message(self,username:str):
        return f"سلام وقت بخیر @{username} \n اکانت بن شده شما آزاد شد. \n لطفا مراقب حجم مصرفیتون باشید که رباط اکانت شما را بن نکند. \n ممنون"

    def not_recoverd_ban_user_message(self,username:str):
        return f"سلام وقت بخیر @{username} \n با عرض پوزش مشکلی در بازشدن اکانت بن شده شما رخ داده لطفا با آیدی {self.admin_telegram_id} تماس حاصل نمایید. \n ممنون"

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

    def read_transfer_users_data(self):
        with open('transfers_brook_list.json', 'r') as openfile:
            # Reading from json file
            json_objects = json.load(openfile)
            openfile.close()

        self.transfers_users_data = json_objects

    def save_transfers_users_data(self):
       transfers_users_list = json.dumps(self.transfers_users_data)
       with open("transfers_brook_list.json", "w") as outfile:
           outfile.write(transfers_users_list)
           outfile.close()
       
       print(f"{cr.Fore.GREEN}All Transfers Users Data Was Writed.")

    def recover_baned_user(self,id:str,username:str):
        counter = 0
        while counter <= 5:
            time.sleep(1)
            result = self.request_recover_user(id)
            if result == True:
                # Send Telegram Message
                telegram_result=self.send_telegram_message(self.recoverd_baned_user_message(username))
                if not telegram_result:
                    print(f"{cr.Fore.RED} Message Not Sended For {username}!!!")

                return True

            counter = counter+1
        
        telegram_result=self.send_telegram_message(self.not_recoverd_ban_user_message(username))
        if not telegram_result:
            print(f"{cr.Fore.RED} Message Not Sended For {username}!!!")

        return False

    def check_users_proccess(self):
        for data in self.transfers_users_data:
            if 'baned_count' in data.keys():
                user_time=int(data['time'])
                if user_time != 0:
                    # Update User Time
                    user_time=user_time-1
                    if user_time > 0:
                        object={'time':user_time}
                        data.update(object)

                        # Write To Json File
                        self.save_transfers_users_data()

                    elif user_time <= 0:
                        object={'time':user_time}
                        data.update(object)

                        # Write To Json File
                        self.save_transfers_users_data()

                        # Recover Baned User
                        revocer_user_result=self.recover_baned_user(data['id'],data['user'])
                        if not revocer_user_result:
                            print(f"{cr.Fore.RED} User {data['user']} Not Recoverd !!!")

                        # Sending Seprator
                        self.send_telegram_message("-"*59)



# -------------------------------------------------------------------------------------------
def start():
    rbu=RecoveryBanedUsers()

    # Get All Transfers Data
    rbu.read_transfer_users_data()

    # Proccess Data
    rbu.check_users_proccess()

    # Sending Seprator
    print(f"{cr.Fore.BLUE}-"*50)

# -------------------------------------------------------------------------------------------
schedule.every(1).minutes.do(start)

while True:
    schedule.run_pending()
    time.sleep(1)