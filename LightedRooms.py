import requests
from requests import Response
from dataclasses import dataclass
import unittest


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


def post_check(date: str, lighted_rooms: list[list[bool]]) -> bool:
    floors_count = len(lighted_rooms)
    flats_on_floor = len(lighted_rooms[0])

    lighted_rooms_count = 0
    lighted_rooms_numbers = []
    for i in range(floors_count):
        for j in range(flats_on_floor):
            if lighted_rooms[i][j]:
                lighted_rooms_count += 1
                lighted_rooms_numbers.append(i * flats_on_floor + j + 1)

    data_to_check = {
        "date": date,
        "data": {
            "count": lighted_rooms_count,
            "rooms": lighted_rooms_numbers
        }
    }

    json = requests.post(Consts.base_url, headers=Consts.headers, json=data_to_check).json()
    return json["message"] == "correct answer"


def get_lighted(date: str) -> (list[list[bool]], bool):
    date_info_json = get_date_info(date).json()
    flats_on_floor = date_info_json["message"]["flats_count"]["data"]
    floors_count = len(date_info_json["message"]["windows"]["data"])
    windows_for_flat = date_info_json["message"]["windows_for_flat"]["data"]
    lighted_windows = [[] for _ in range(floors_count)]

    for i in range(floors_count):
        lighted_windows[i] = date_info_json["message"]["windows"]["data"][f"floor_{i + 1}"]

    lighted_rooms = [[False for _ in range(flats_on_floor)] for _ in range(floors_count)]

    for i in range(floors_count):
        for j in range(flats_on_floor):
            for w in range(windows_for_flat[j]):
                count = 0
                for n in range(j):
                    count += windows_for_flat[n]

                if lighted_windows[i][count + w]:
                    lighted_rooms[i][j] = True

    return lighted_rooms, post_check(date, lighted_rooms)


def get_flat_number_in_floor(windows_for_flat: list[int], window: int) -> int:
    for i in range(len(windows_for_flat)):
        window -= windows_for_flat[i]
        if window < 0:
            return i + 1


def get_windows(date: str) -> list[list[(bool, int)]]:
    date_info_json = get_date_info(date).json()
    flats_on_floor = date_info_json["message"]["flats_count"]["data"]
    floors_count = len(date_info_json["message"]["windows"]["data"])
    windows_for_flat = date_info_json["message"]["windows_for_flat"]["data"]
    lighted_windows = [[] for _ in range(floors_count)]

    for i in range(floors_count):
        lighted_windows[i] = date_info_json["message"]["windows"]["data"][f"floor_{i + 1}"]

    windows_with_number = [[[False, 0] for _ in range(sum(windows_for_flat))] for _ in range(floors_count)]
    for i in range(floors_count):
        for j in range(sum(windows_for_flat)):
            windows_with_number[i][j][0] = lighted_windows[i][j]
            windows_with_number[i][j][1] = i * flats_on_floor + get_flat_number_in_floor(windows_for_flat, j)

    return windows_with_number


class Tests(unittest.TestCase):
    def test_get_lighted(self):
        json = get_dates().json()
        dates = json["message"]

        for date in dates:
            lighted_rooms, correct = get_lighted(date)

            self.assertTrue(correct, f"On date {date} lighted rooms are incorrect")
