import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv


class SymmetricHandler:

    load_dotenv()
    __temp_key = (os.getenv('TEMP_KEY')).encode('utf-8')

    def __init__(self, password):
        self.__password = password
        self.__token_dc = None
        self.__token_ec = None

    @property
    def password(self):
        return self.__password

    def __encrypt(self):
        if not SymmetricHandler.__type_check(self.password):
            self.__token_ec = Fernet(self.__temp_key).encrypt(self.__password.encode('utf-8'))
        else:
            raise Exception("Expected String !")

    def __decrypt(self):
        if SymmetricHandler.__type_check(self.__token_ec):
            self.__token_dc = Fernet(self.__temp_key).decrypt(self.__token_ec)
        else:
            raise Exception("Expected bytearray !")

    @staticmethod
    def __type_check(value):
        if isinstance(value, bytes):
            return True
