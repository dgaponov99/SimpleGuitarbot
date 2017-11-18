import ConstantValues
import requests
import json

token = ConstantValues.TOKEN
URL = 'https://api.telegram.org/bot%s/' % token


def get_updates():
    url = URL + 'getupdates'
    r = requests.get(url)
    return r.json()


def main():
    send_messages()
    # d=get_updates()
    # with open('updates.json','w') as file:
    #   json.dump(d,file,indent=4,ensure_ascii=False)


def get_messages():
    data = get_updates()
    chat_id = data['result'][-1]['message']['chat']['id']
    message_text = data['result'][-1]['message']['text']
    message = {'chat_id': chat_id, 'message_text': message_text}
    return message


def send_messages():
    answer = get_messages()
    url = URL + 'sendmessage?chat_id={}&text={}'.format(answer['chat_id'], answer['message_text'])
    requests.get(url)


main()
