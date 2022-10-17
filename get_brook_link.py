import requests
import json

signin_url='https://irvpn.co/userapi/signin'

print("Enter The Username: ")
username=input()
print("Enter The Password: ")
password=input()

post_data = {'username': username,'password':password}

res = requests.post(signin_url,json=post_data)
if str(res)=="<Response [200]>":
    data=json.loads(res.text)
    link=f"https://irvpn.co/brook_link.txt?token={data['token']}&level=0"
    res2=requests.get(link)
    prime_link=res2.text.replace("198.244.140.109","195.28.11.20")
    print(prime_link)
else:
    print("Wrong!")
    print(res)
    print(res.text)