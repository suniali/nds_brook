import requests
import json

signup_url='https://irvpn.co/userapi/signup'
signin_url='https://irvpn.co/userapi/signin'

print("Enter The Username: ")
username=input()
username=username.replace('@','')
# print(f"this is username{username}")
password=f'nds_{username}_2022'

post_data = {'username': username,'password':password}

res = requests.post(signup_url, json = post_data)

if str(res)=="<Response [200]>" :
    print(f"{username} Was SignedUp Successfully.")

    print("Crating Link...")
    res2 = requests.post(signin_url,json=post_data)
    if str(res2)=="<Response [200]>":
        data=json.loads(res2.text)
        link=f"https://irvpn.co/brook_link.txt?token={data['token']}&level=0"
        res3=requests.get(link)
        prime_link=res3.text.replace("198.244.140.109","195.28.11.20")
        print("Connection Link Is:")
        print(prime_link)
        # Writing Data To File
        s=f"username: {username} password: {password} link: {prime_link}"
        with open("nds_brook_username_password_list.txt", "a") as myfile:
            myfile.write(s + "\n")
            myfile.close()
    else:
        print("Wrong!")
        print(res)
        print(res.text)

else :
    print("The SignUp Was Failed!")
    print(res)

