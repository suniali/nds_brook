import json
import mysql.connector
import colorama as cr
from mysql.connector import Error

cr.init(autoreset=True)

print("Enter Username : ")
username=input()

try:
    connection = mysql.connector.connect(host='198.244.140.109',
                                         database='brook',
                                         user='jarvis',
                                         password='MH75d$4s#d9.f6bF')
    if connection.is_connected():
        cursor = connection.cursor()
        query="SELECT * FROM user"
        cursor.execute(query)
        res=cursor.fetchall()

        # Opening JSON file
        with open('transfers_brook_list.json', 'r') as openfile:
            # Reading from json file
            json_objects = json.load(openfile)

        for row in res:
            for data in json_objects:
                if data['user']==row[1]:
                    if data['user']==username:
                        last_transfer=int(data['transfer'])
                        current_transfer=int(row[7])
                        calc=current_transfer-last_transfer
                        
                        print(f"Transaction for user {cr.Fore.GREEN}{data['user']} is {cr.Fore.CYAN}{calc}")
                        # exit from script
                        exit()
except Error as e:
    print(f"{cr.Fore.RED}Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")


 