import requests

url = 'https://olimp.miet.ru/ppo_it_final'
getheads = {
    'X-Auth-Token': 'ppo_10_10320',
}
getparams = {
}
response = requests.get(url=url, params=getparams, headers=getheads)
data = response.json()
print(data)
