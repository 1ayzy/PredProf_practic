import requests

url = 'https://olimp.miet.ru/ppo_it_final'
getheads = {
    'X-Auth-Token': 'ppo_10_10320',
}

getparams = {
    'day': '25',
    'month': '01',
    'year': '23',
}

response = requests.get(url=url, params=getparams, headers=getheads)
data = response.json()
print(data)
