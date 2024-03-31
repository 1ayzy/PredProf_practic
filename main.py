from dataclasses import dataclass

import requests
from requests import Response


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


    def post_check(data_to_check: dict) -> Response:
        return requests.post(Consts.base_url, headers=Consts.headers, json=data_to_check)


    def get_lighted(date: str) -> (list[list[bool]], int, list[int]):
        date_info_json = Consts.get_date_info(date).json()
        flats_on_floor = date_info_json["message"]["flats_count"]["data"]
        floors_count = len(date_info_json["message"]["windows"]["data"])
        windows_for_flat = date_info_json["message"]["windows_for_flat"]["data"]
        lighted_windows = list(date_info_json["message"]["windows"]["data"].values())

        lighted_rooms = [[False for _ in range(flats_on_floor)] for _ in range(floors_count)]

        for i in range(floors_count):
            for j in range(flats_on_floor):
                for w in range(windows_for_flat[j]):
                    count = 0
                    for n in range(j):
                        count += windows_for_flat[n]

                    if lighted_windows[i][count + w]:
                        lighted_rooms[i][j] = True

        lighted_rooms_count = 0
        lighted_rooms_numbers = []
        for i in range(floors_count):
            for j in range(flats_on_floor):
                if lighted_rooms[i][j]:
                    lighted_rooms_count += 1
                    lighted_rooms_numbers.append(i * flats_on_floor + j + 1)

        return lighted_rooms, lighted_rooms_count, lighted_rooms_numbers


    def program_test() -> dict[str, bool]:
        json = Consts.get_dates().json()

        dates = json["message"]

        ret = {}

        for i in dates:
            lighted_rooms, lighted_rooms_count, lighted_rooms_numbers = Consts.get_lighted(i)

            data_to_check = dict()
            data_to_check["date"] = i
            data_to_check["data"] = {
                "count": lighted_rooms_count,
                "rooms": lighted_rooms_numbers
            }

            resp = Consts.post_check(data_to_check).json()

            ret[i] = resp["message"] == "correct answer"

        return ret


if __name__ == '__main__':
    print(Consts.program_test())
