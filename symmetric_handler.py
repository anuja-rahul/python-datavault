import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv


class SymmetricHandler:

    load_dotenv()
    __temp_key = (os.getenv('TEMP_KEY')).encode('utf-8')

    def __init__(self, password: str):
        self.__password = password
        self.__token_dc = None
        self.__token_ec = None

    @property
    def password(self) -> str:
        return self.__password

    def get_token(self, byte: bool = True) -> any:
        if byte:
            return self.__token_ec
        else:
            return self.__token_ec.decode('utf-8')

    def __encrypt(self) -> None:
        if not SymmetricHandler.__type_check(self.password):
            self.__token_ec = Fernet(self.__temp_key).encrypt(self.__password.encode('utf-8'))
        else:
            raise Exception("Expected String !")

    def __decrypt(self) -> None:
        if SymmetricHandler.__type_check(self.__token_ec):
            self.__token_dc = Fernet(self.__temp_key).decrypt(self.__token_ec)
        else:
            raise Exception("Expected bytes !")

    @staticmethod
    def __type_check(value: any) -> bool:
        if isinstance(value, bytes):
            return True
        else:
            return False
