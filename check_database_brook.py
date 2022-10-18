import json
import telepot
from lib2to3.pgen2 import token
import mysql.connector
import colorama as cr
from mysql.connector import Error

cr.init(autoreset=True)

token='5677357335:AAGauZANKo0qIspAMXJIPLqUixlrqYuhZ9Y'

limit_users_transfer=1024
limit_vip_users_transfer=5120
warning_users_transfer=700
warning_vip_users_transfer=4000

vip_users=['jarvis_sky','Aliafagh']
ultimate_user='mortezaparsa'

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
            if row[1]!=ultimate_user:
                for data in json_objects:
                    if data['user']==row[1]:
                        last_transfer=int(data['transfer'])
                        current_transfer=int(row[7])
                        calc=current_transfer-last_transfer
                        for vip_user in vip_users:
                            if data['user']==vip_user:
                                if calc > limit_vip_users_transfer:
                                    # User Should Be Banne
                                    s=f"user: {row[1]} transfer: {calc}"
                                    print(f"{cr.Fore.RED}Max Transfer Found On {cr.Fore.CYAN}VIP {cr.Fore.YELLOW}{s}")
                                    if "id" in data:
                                        reciver_id=data['id']
                                        bot=telepot.Bot(token)
                                        bot.sendMessage(reciver_id,"سلام وقت بخیر \n با عرض پوزش اکانت شما بن شد")
                                    else:
                                        print(f"{cr.Fore.MAGENTA}ID Is Not Exitst For {cr.Fore.CYAN}{data['user']} {cr.Fore.MAGENTA}And Message Not Sent!")
                                elif calc > warning_vip_users_transfer:
                                    # Send Warning Message
                                    s=f"user: {row[1]} transfer: {calc}"
                                    print(f"{cr.Fore.YELLOW}Warning for {cr.Fore.CYAN}VIP {cr.Fore.WHITE}{s}")
                                    if "id" in data:
                                        reciver_id=data['id']
                                        bot=telepot.Bot(token)
                                        bot.sendMessage(reciver_id,f"سلام وقت بخیر \n هشدار بن اکانت : شما تا الان {calc} مگابایت مصرف کرده اید")
                                    else:
                                        print(f"{cr.Fore.MAGENTA}ID Is Not Exitst For {cr.Fore.CYAN}{data['user']} {cr.Fore.MAGENTA}And Message Not Sent!")

                                # exit from loop after user doesn't touch limit
                                break
                        # print(f"user: {data['user']} calc : {calc}")
                        if calc > limit_users_transfer:
                            # User Should Be Banne
                            s=f"user: {row[1]} transfer: {calc}"
                            print(f"{cr.Fore.RED}Max Transfer Found On {cr.Fore.YELLOW}{s}")
                            if "id" in data:
                                reciver_id=data['id']
                                bot=telepot.Bot(token)
                                bot.sendMessage(reciver_id,"سلام وقت بخیر \n با عرض پوزش اکانت شما بن شد")
                            else:
                                print(f"{cr.Fore.MAGENTA}ID Is Not Exitst For {cr.Fore.CYAN}{data['user']} {cr.Fore.MAGENTA}And Message Not Sent!")
                       
                        elif calc > warning_users_transfer:
                            # Send Warning Message
                            s=f"user: {row[1]} transfer: {calc}"
                            print(f"{cr.Fore.YELLOW}Warning for {cr.Fore.WHITE}{s}")
                            if "id" in data:
                                reciver_id=data['id']
                                bot=telepot.Bot(token)
                                bot.sendMessage(reciver_id,f"سلام وقت بخیر \n هشدار بن اکانت : شما تا الان {calc} مگابایت مصرف کرده اید")
                            else:
                                print(f"{cr.Fore.MAGENTA}ID Is Not Exitst For {cr.Fore.CYAN}{data['user']} {cr.Fore.MAGENTA}And Message Not Sent!")
                        
                        # exit from loop after user doesn't touch limit
                        break

except Error as e:
    print(f"{cr.Fore.RED}Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
