from abc import abstractmethod, ABC

from cryptography.fernet import Fernet


class Cryptographer(ABC):
    @abstractmethod
    def encrypt(self, data):
        pass

    @abstractmethod
    def decrypt(self, data):
        pass


class FernetCryptographer(Cryptographer):

    def __init__(self, key):
        self._fernet = Fernet(key)

    def encrypt(self, data):
        return self._fernet.encrypt(data)

    def decrypt(self, data):
        return self._fernet.decrypt(data)
