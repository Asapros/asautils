from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from pickle import dump, load, dumps, loads
class Serializable(object):
    def save(self, file: str) -> bool:
        """Saving serialized list in a file
Returning result of operation
"""
        try:
            dump(self, open(file, "wb"))
            return True
        except:
            return False
    def load(self, file: str) -> bool:
        """Loading serialized list from a file
Returning result of operation
"""
        try:
            self.__dict__.update(load(open(file, "rb")).__dict__)
            return True
        except:
            return False
    def saveEncoded(self, file: str, key: str):
        """Saving encrypted 'self' in 'file'"""
        open(file, "wb").write(self.encode(key))
    def loadDecoded(self, file: str, key: str):
        """Replacing 'self' with decrypted content of 'file'"""
        self.decode(open(file, "rb").read(), key)
    def encode(self, key: str):
        """Returning encrypted version of self"""
        return Fernet(self.__getKey(key)).encrypt(dumps(self))
    def decode(self, bytetext: bytes, key: str):
        """Replacing self with decoded 'bytetext'"""
        self.__dict__.update(loads(Fernet(self.__getKey(key)).decrypt(bytetext)).__dict__)

    def __getKey(self, text: str):
        """Generating a two-way key for encryption and decryption from plain text
Inserting key longer than 32 bytes will cut it to 32 only characters
Inserting key shorter than 32 bytes will fill it with nulls to lenght 32
"""
        paddedtext = text + chr(0)*(32-len(text)) # Adding null characters to fill key to 32 bytes
        paddedtext = paddedtext[:32] # If 'text' argument is too long it's now cutting to 32 characters
        return urlsafe_b64encode(paddedtext.encode("utf-8")) # Returning key

