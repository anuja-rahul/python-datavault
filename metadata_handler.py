import json


class MetadataHandler:

    __metadata_file = "FileData.json"
    __template_file = {
        "filenames": [],
        "passwords": []
    }

    def __init__(self, filename: list, password: bytearray):
        self.__temp_filename = filename
        self.__filenames = None
        self.__temp_password = password
        self.__passwords = None
        self.__json_data = {}

    def __set_template(self):
        self.__json_data["filenames"] = self.__filenames
        self.__json_data["password"] = self.__password

    def __dump_to_json(self):
        with open(MetadataHandler.__metadata_file, 'w') as file:
            file.write(json.dumps(self.__json_data, indent=2))

    def __load_from_json(self):
        with open(MetadataHandler.__metadata_file, 'r') as file:
            self.__json_data = json.loads(file.read())

        self.__filenames = self.__json_data["filenames"]
        self.__password = self.__json_data["password"]

    def update_metadata(self):
        if self.__temp_filename not in self.__filenames:
            self.__filenames.append(self.__temp_filename)
        if self.__temp_password not in self.__passwords:
            self.__passwords.append(self.__temp_password)
