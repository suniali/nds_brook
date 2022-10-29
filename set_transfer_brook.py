import json
import time
import schedule
import mysql.connector
import colorama as cr
from mysql.connector import Error

cr.init(autoreset=True)

class SetData:
    def __init__(self) -> None:
        pass

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

       return json_objects

    def write_transfers_users_data(self,users_data:list) -> None:
        d=self.read_transfer_users_data()
        #Writing To Transfer Brook List Database
        for data in users_data:
            for user in d:
                if data[1]== user['user']:
                    s={"transfer": data[7]}
                    user.update(s)
                    break

        # print(d)
        json_object = json.dumps(d)
        with open("transfers_brook_list.json", "w") as outfile:
            outfile.write(json_object)

        print(f"{cr.Fore.GREEN}Data Downloaded Successfuly.")     

    def read_permanent_baned_users(self):
        with open('permanent_ban_users.txt', 'r') as openfile:
            # Reading from json file
            baned_users_list = openfile.readlines()
            openfile.close()

        return baned_users_list

    def reset_baned_users_file(self)->None:
        # Read Permanent Baned Users File
        permanent_baned_users=self.read_permanent_baned_users()

        # Rest Baned Users List Text File
        with open('baned_users_list.txt', 'w') as openfile:
            # Writing from List
            for user in permanent_baned_users:
                temp_user_info = user.split(',')
                u = f"{temp_user_info[0]},{temp_user_info[1]}"
                openfile.write(u)

            openfile.close()



def start():
    sd = SetData()
    get_users_result = sd.get_users()

    if get_users_result is False:
        print(f"{cr.Fore.RED}Users Info Was Not Downloaded!!!")
        exit()

    else:
        sd.write_transfers_users_data(get_users_result)
        sd.reset_baned_users_file()
                

    

# -------------------------------------------------------------------------------------------
schedule.every(1).minute.do(start)

while True:
    schedule.run_pending()
    time.sleep(1)