import json
import os
from flask import Flask, jsonify

ID_JSON = "./data_text.json"
INSTANCE_JSON = "./inst.json"


class ExistIDManager:
    def __init__(self, file_name="./data_test.json") -> None:
        self._file_path = file_name
        self._data = self.__process_file()

    def id_exist(self, id):
        return str(id) in self._data

    def add(self, key):
        self._data[str(key)] = key
        self.__update_file()

    def __update_file(self):
        file_path = self._file_path
        with open(file_path, "w") as file:
            json.dump(self._data, file)
            file.close()

    def __process_file(self,):
        file_path = self._file_path
        if os.path.exists(file_path):
            if file_path.endswith('.json'):
                with open(file_path, 'r') as file:
                    text = file.read()
                try:
                    json_obj = json.loads(text)
                    return json_obj
                except json.JSONDecodeError:
                    return {"error": "Invalid JSON format in text file"}
            else:
                return {"error": "File exists but is not a .txt file"}
        else:
            default_content = {}
            with open(file_path, 'w') as file:
                json.dump(default_content, file)
            return default_content


class InstanceManager:
    def __init__(self, filePath="./inst_test.json") -> None:
        self._file_path = filePath
        self._data = self.__process_file()

    def ins_info(self, id):
        if str(id) in self._data:
            return self._data[str(id)]["curr"]
        else:
            return self.crate_ins(id)

    def crate_ins(self, id="1"):
        self._data[str(id)] = {"curr": 100000}
        self.__update_file()
        return self._data[str(id)]["curr"]

    def upadte_last(self, id, value):
        self._data[str(id)]["curr"] = value
        self.__update_file()
        return 200

    def __update_file(self):
        file_path = self._file_path
        with open(file_path, "w") as file:
            json.dump(self._data, file)
            file.close()

    def __process_file(self,):
        file_path = self._file_path
        if os.path.exists(file_path):
            if file_path.endswith('.json'):
                with open(file_path, 'r') as file:
                    text = file.read()
                try:
                    json_obj = json.loads(text)
                    return json_obj
                except json.JSONDecodeError:
                    return {"error": "Invalid JSON format in text file"}
            else:
                return {"error": "File exists but is not a .txt file"}
        else:
            default_content = {}
            with open(file_path, 'w') as file:
                json.dump(default_content, file)
            return default_content


app = Flask(__name__)
id_manager = ExistIDManager(ID_JSON)
instanceManager = InstanceManager(INSTANCE_JSON)


@app.route("/datas", methods=["GET"])
def get_all_data():
    return jsonify(id_manager._data), 200


@app.route('/id/<int:id>', methods=['GET'])
def check_id(id):
    return str(id_manager.id_exist(id)), 200


@app.route('/add/<int:id>', methods=['GET'])
def add_id(id):
    id_manager.add(id)
    return "Done.", 200


@app.route('/i/<int:id>', methods=['GET'])
def ins_info(id):
    inst_info = instanceManager.ins_info(id)
    return f'{inst_info}', 200


@app.route('/i/<int:id>/c/<int:num>', methods=['GET'])
def add_ins_info(id, num):
    instanceManager.upadte_last(id, num)
    return f'200', 200


if __name__ == '__main__':
    app.run(debug=True)
