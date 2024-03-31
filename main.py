import requests
r = requests.get("https://olimp.miet.ru/ppo_it_final/date", headers={"X-Auth-Token": "ppo_9_19633"})

print(r.text)