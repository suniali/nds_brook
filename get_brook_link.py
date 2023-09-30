import requests
import json

signin_url='https://irvpn.co:9991/userapi/signin'
brook_get_link='https://irvpn.co:9991/brook_link.txt?token='

print("Enter The Username: ")
username=input()
# print("Enter The Password: ")
# password=input()
password=f"nds_{username}_2022"

post_data = {'username': username,'password':password}

res = requests.post(signin_url,json=post_data)
if str(res)=="<Response [200]>":
    data=json.loads(res.text)
    link=f"{brook_get_link}{data['token']}&level=0"
    res2=requests.get(link)
    # prime_link=res2.text.replace("198.244.140.109","195.28.11.20")
    prime_link=res2.text
    print(prime_link)
else:
    print("Wrong!")
    print(res)
    print(res.text)