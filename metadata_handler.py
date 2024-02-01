import os
import json
from datalogger import DataLogger


class MetadataHandler:

    __metadata_file = "FileData.json"
    __template_file = {
        "filenames": [],
        "passwords": []
    }
    __temp_files = os.listdir()

    def __init__(self, filename: list[str], password: list[bytes]):
        self.init_env()

        self.__temp_filename = filename
        self.__filenames = []
        self.__temp_password = password
        self.__passwords = []
        self.__json_data = {}

        self.save_metadata()

    @staticmethod
    def init_env():
        if MetadataHandler.__metadata_file not in MetadataHandler.__temp_files:
            with open(MetadataHandler.__metadata_file, "w") as file:
                file.write(json.dumps(MetadataHandler.__template_file, indent=2))

    def __set_template(self):
        self.__json_data["filenames"] = self.__filenames
        self.__json_data["password"] = self.__password

    @DataLogger.logger
    def __dump_to_json(self):
        with open(MetadataHandler.__metadata_file, 'w') as file:
            file.write(json.dumps(self.__json_data, indent=2))

    @DataLogger.logger
    def __load_from_json(self):
        with open(MetadataHandler.__metadata_file, 'r') as file:
            self.__json_data = json.loads(file.read())

        if self.__json_data is not None:
            self.__filenames = self.__json_data["filenames"]
            self.__password = self.__json_data["passwords"]

    @DataLogger.logger
    def __update_metadata(self):
        if self.__temp_filename not in self.__filenames:
            self.__filenames += self.__temp_filename
        if self.__temp_password not in self.__passwords:
            self.__passwords += self.__temp_password

    def save_metadata(self):
        self.__load_from_json()
        self.__update_metadata()
        self.__dump_to_json()

    def __repr__(self):
        return f"[{self.__temp_filename}, {self.__temp_password}]"
