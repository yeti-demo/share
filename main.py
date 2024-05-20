import requests as req
from os import path, mkdir
import json
import time

BASE_URL = "http://localhost:5000"


class ExistIDManager:
    def __init__(self, inst_id=1) -> None:
        self._instance_id = inst_id
        self._data = self.__import_data()
        self._instance_start = self.__instance_info()

    def save_instance_checked(self, id):
        res = req.get(f'{BASE_URL}/i/{self._instance_id}/c/{id}')
        res.raise_for_status()

    def save_exist(self, id):
        res = req.get(f'{BASE_URL}/add/{id}')
        res.raise_for_status()

    def __import_data(self):
        res = req.get(f'{BASE_URL}/datas')
        if res.status_code == 200:
            return res.json()
        else:
            return res.raise_for_status()

    def __instance_info(self):
        res = req.get(f'{BASE_URL}/i/{self._instance_id}')
        res.raise_for_status()
        return int(res.text)

    def id_exist(self, id):
        return str(id) in self._data


def get_url(id=616305):
    return f'https://ncmym.edu.bd/application/preview?uid={id}&type=honours'
    # return f'http:localhost:8080/user?id={id}'


def save_it(id, text):
    with open(f'./html/{id}.html', 'w', encoding='utf-8') as file:
        file.write(text)
        file.close()


def update_exist(data):
    with open("./data.json", "w") as file:
        json.dump(data, file)


def main_x():
    start_from = int(input("Start from : "))
    current_id = start_from
    while(True):
        res = req.get(get_url(current_id))
        if (res.status_code == 200):
            print(f'{current_id} - Found')
            save_it(current_id, res.text)
        else:
            print(f'{current_id} - Not found')

        # time.sleep(0.5)
        # break
        current_id += 1


def main():
    instent_id = "1" or str(input("Instance id : (1)")) or 1
    data = ExistIDManager(inst_id=instent_id)
    curr_id = int(data._instance_start)
        
    while(True):
        if data.id_exist(curr_id):
            print(f'{curr_id} - Already exist')
            curr_id += 1
            continue
        res = req.get((get_url(curr_id)))

        if res.status_code == 200:
            print(f'{curr_id} - Found')
            save_it(curr_id, res.text)
            data.save_exist(curr_id)
        else:
            print(f'{curr_id} - Not Found')

        data.save_instance_checked(curr_id)
        curr_id += 1


if __name__ == "__main__":
    try:

        main()
    except KeyboardInterrupt:
        exit()
    except Exception as err:
        print(err)
        exit()
