#!/bin/env python3.6
import requests, json, sys, time


VK_API_URL = 'https://api.vk.com/'

# https://oauth.vk.com/authorize?client_id=5494844&display=page&redirect_uri=http://localhost/copy-your-access-token/but-dont-commit-it&response_type=token&v=5.76&state=123456
ACCESS_TOKEN = ''


def obj(dct):
    a = lambda: dct
    a.__dict__.update(dct)
    return a


def vk(method, **params):
    defaults = dict(v=5.52, access_token=ACCESS_TOKEN)
    defaults.update(params)
    query = ['{}={}'.format(k, v) for k, v in defaults.items()]
    query = 'method/{}?{}'.format(method, '&'.join(query))
    time.sleep(0.3) # bypassing 'Too many requests per second'
    body = requests.get(VK_API_URL + query).text
    json2 = json.loads(body)
    if 'error' in json2:
        raise ValueError(json2['error'])
    return json2


def vkr(method, **params):
    response_dict = vk(method, **params)['response']
    return response_dict


def main(uid):
    user_defaults = {'hidden':1}
    user_defaults.update(vkr('users.get', user_ids=uid, fields='online')[0])
    user = obj(user_defaults)
    print("Имя Вконтакте:", user.first_name, user.last_name)
    print("Адрес:", 'vk.com/id' + str(user.id))
    print("Скрытый пользователь:", "да" if user.hidden else "нет")
    friends = obj(vkr('friends.get', user_id=user.id, order='hints', count=12))
    print("Друзей:", friends.count)
    print("Top 12 друзей:")
    for i, friend_id in enumerate(friends.items):
        friend = obj(vkr('users.get', user_ids=friend_id)[0])
        print('{}) {} {}'.format(i+1, friend.first_name, friend.last_name))
     


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('\tusage: vk.py suninaries')
        print('\tusage: vk.py 295426804')
        sys.exit(1)
    else:
        link = sys.argv[1]
        main(link)