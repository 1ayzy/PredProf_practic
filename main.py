import requests

url = 'https://olimp.miet.ru/ppo_it_final'
getparams = {
    'X-Auth-Token': 'ppo_10_10320',
}
response = requests.get(url=url, params=getparams)
data = response.json()
print(data)
