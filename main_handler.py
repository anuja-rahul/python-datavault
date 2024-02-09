from symmetric_handler import SymmetricHandler, AESCipherHandler
from metadata_handler import MetadataHandler

from python_datalogger import DataLogger


class MainHandler:
    def __init__(self, path: str, password: str):
        self.__path = path
        self.__ext = None
        self.__password = password
        self.__byte_data = None
        self.logger = DataLogger(name="MainHandleLogger", propagate=True)

    @property
    def path(self):
        return self.__path

    @property
    def password(self):
        return self.__password

    def __get_password_token(self):
        sym_handler = SymmetricHandler(password=self.__password)
        sym_handler.encrypt()
        pwd_token = sym_handler.get_token(byte=True).decode('utf-8')
        return pwd_token

    def encrypt(self):
        if self.__path is not None:
            self.__read_file()
            aes_en_handler = AESCipherHandler(password=self.__password, logger_name="CryptoHandleLogger(EN)")
            aes_en_handler.assign_salt()
            aes_en_handler.generate_key()
            aes_en_handler.write_to_bin(file_name=f"{self.__path}.bin", data=aes_en_handler.encrypt(self.__byte_data))
            aes_en_handler.salt_to_bin(path=f"{self.__path}.salt.bin")

            pwd_token = self.__get_password_token()
            MetadataHandler(filename=self.__path, password=pwd_token, status="EC")

        else:
            raise Exception("No path provided !")

    def decrypt(self):
        if self.__path is not None:
            aes_dc_handler = AESCipherHandler(password=self.__password, logger_name="CryptoHandleLogger(DC)")
            paths = self.__get_sorted_path()
            aes_dc_handler.get_salt(path=f"{paths[0]}.{paths[1]}.salt.bin")
            aes_dc_handler.generate_key()
            ec_data = aes_dc_handler.read_from_bin(file_name=self.__path)
            dc_data = aes_dc_handler.decrypt(data=ec_data)

            if self.__write_to_file(path=f"{paths[0]}.{paths[1]}", data=dc_data):
                pwd_token = self.__get_password_token()
                MetadataHandler(filename=f"{paths[0]}.{paths[1]}", password=pwd_token, status="DC")

    def __get_sorted_path(self):
        return self.__path.split(".")

    @DataLogger.logger
    def __read_file(self):
        with open(self.__path, 'rb') as file:
            self.__byte_data = file.read()

    def __write_to_file(self, path: str, data: bytes):
        try:
            with open(path, 'wb') as file:
                file.write(data)

            return True
        except Exception as error:
            self.logger.log_error(f"{error}")
