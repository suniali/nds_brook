import json
import mysql.connector
import colorama as cr
from mysql.connector import Error

cr.init(autoreset=True)

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

        d=[]
        #Writing to database
        for row in res:
            s={"user": row[1],"transfer": row[7]}
            d.append(s)
            
        # print(d)
        json_object = json.dumps(d)
        # print(json_object)
        with open("transfers_brook_list.json", "w") as outfile:
            outfile.write(json_object)

        print(f"{cr.Fore.GREEN}Data Downloaded Successfuly.")

except Error as e:
    print(f"{cr.Fore.RED}Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
