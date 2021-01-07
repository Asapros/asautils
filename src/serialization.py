"""
Requires 'cryptography' module to work.
All 'extypes' extends 'Serializable' ( help(asautils.extypes) )

Examples:
    # Saving object in a file
    obj = EXlist(["a", "b", "c"])
    obj.save("obj.bin")
    del obj
    obj = load("obj.bin")
    print(obj)
    >>> ["a", "b", "c"]
    # Saving encrypted object in a file
    obj = EXstr("SuperSecretString")
    obj.saveEncrypted("obj.bin", "SuperSecretPassword")
    del obj
    # Wrong password will raise a 'InvalidToken' error
    obj = loadDecrypted("obj.bin", "SuperSecretPassword")
    print(obj)
    >>> SuperSecretString
"""
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
from pickle import dump, load, dumps, loads
class Serializable:
    def save(self, file: str) -> bool:
        """Saving serialized object in a file"""
        dump(self, open(file, "wb"))
    
    def saveEncrypted(self, file: str, key: str):
        """Saving encrypted 'self' in 'file'"""
        open(file, "wb").write(self.encrypt(key))
    
    def encrypt(self, key: str):
        """Returning encrypted version of self"""
        return Fernet(getKey(key)).encrypt(dumps(self))

def load(file: str):
    """Returns object loaded from a file"""
    return loads(open(file, "rb").read())
def loadDecrypted(file: str, key: str):
    """Returns decrypted content of 'file'"""
    return decrypt(open(file, "rb").read(), key)
def decrypt(bytetext: bytes, key: str):
    """Returning decrypted 'bytetext'"""
    return loads(Fernet(getKey(key)).decrypt(bytetext))
def getKey(text: str):
    """Generating a two-way key for encryption and decryption from plain text
Inserting key longer than 32 bytes will cut it to 32 only characters
Inserting key shorter than 32 bytes will fill it with nulls to lenght 32
"""

    paddedtext = text + chr(0)*(32-len(text))
    # ^ Adding null characters to fill key to 32 bytes
    paddedtext = paddedtext[:32]
    # ^ If 'text' argument is too long it's now cutting to 32 characters
    return urlsafe_b64encode(paddedtext.encode("utf-8"))
    # ^ Returning key

    
    
