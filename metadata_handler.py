import os
import json
from python_datalogger import DataLogger


class MetadataHandler:

    __metadata_file = "FileData.json"
    __template_file = {
        "FileData": []
    }
    __temp_files = os.listdir()

    def __init__(self, filename: str, password: str, status: str):
        self.init_env()

        self.__temp_filename = filename
        self.__temp_password = password
        self.__status = status
        self.__temp_array = {"filename": self.__temp_filename, "password": self.__temp_password,
                             "status": self.__status}
        self.__current_array = []
        self.__json_data = {}

        self.save_metadata()

    @classmethod
    def init_env(cls):
        if MetadataHandler.__metadata_file not in MetadataHandler.__temp_files:
            with open(MetadataHandler.__metadata_file, "w") as file:
                file.write(json.dumps(MetadataHandler.__template_file, indent=2))

    @DataLogger.logger
    def __load_from_json(self):
        with open(MetadataHandler.__metadata_file, 'r') as file:
            self.__json_data = json.loads(file.read())

        if self.__json_data["FileData"] is not None:
            self.__current_array = self.__json_data["FileData"]

    @DataLogger.logger
    def __dump_to_json(self):
        with open(MetadataHandler.__metadata_file, 'w') as file:
            file.write(json.dumps(self.__json_data, indent=3))

    @DataLogger.logger
    def __update_metadata(self):
        if len(self.__current_array) > 0:
            for arrays in self.__current_array:
                if (not arrays['filename'] == self.__temp_array['filename'] and
                        arrays['password'] == self.__temp_array['password']):
                    self.__current_array.append(self.__temp_array)
                else:
                    if arrays['status'] != self.__temp_array['status']:
                        self.__current_array.remove(arrays)
                        self.__current_array.append(self.__temp_array)
        else:
            self.__current_array.append(self.__temp_array)

        self.__json_data["FileData"] = self.__current_array

    def save_metadata(self):
        self.__load_from_json()
        self.__update_metadata()
        self.__dump_to_json()

    def __repr__(self):
        return f"[{self.__temp_filename}, {self.__temp_password}]"
