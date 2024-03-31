import requests
from requests import Response
from dataclasses import dataclass


@dataclass
class Consts:
    base_url = "https://olimp.miet.ru/ppo_it_final"
    headers = {"X-Auth-Token": "ppo_9_19633"}


def get_dates() -> Response:
    return requests.get(Consts.base_url + "/date", headers=Consts.headers)


def get_date_info(date: str) -> Response:
    day, month, year = date.split("-")
    params = {"day": day, "month": month, "year": year}
    return requests.get(Consts.base_url, headers=Consts.headers, params=params)


print("get_dates")
json = get_dates().json()
print("dates good")

data = json["message"][0]

print(f"date info: {data}")
r = get_date_info(data)


print(r.text)
