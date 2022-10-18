import json
import requests
import colorama as cr

cr.init(autoreset=True)

users=[]
url="https://api.telegram.org/bot5677357335:AAGauZANKo0qIspAMXJIPLqUixlrqYuhZ9Y/getUpdates"

res=requests.get(url=url)
if str(res)=="<Response [200]>":
    datas=json.loads(res.text)['result']
    for data in datas:
        if "message" in data:
            if data['message']['from']["id"]:
                id=data['message']['from']["id"]
                username=data['message']['from']["username"]
                item={"user":username,"id":id}
                users.append(item)

    # # Remove Duplicate Items
    # unic_users=[*set(users)]

    # Reading database
    with open('transfers_brook_list.json', 'r') as openfile:
        # Reading from json file
        json_objects = json.load(openfile)
    
    for object in json_objects:
        for user in users:
            if object['user']==user['user']:
                object.update({"id":user['id']})
                break
    
    # Writing file
    writable_data=json.dumps(json_objects)
    with open("transfers_brook_list.json", "w") as outfile:
        outfile.write(writable_data)

    print(f"{cr.Fore.CYAN}Update All Data Successfully.")
else:
    print(f"{cr.Fore.RED}{res}")