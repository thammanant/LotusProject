import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv


class Decryption:
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('KEY')

    def decrypt(self, message):
        # TODO remove comments when done testing
        # fernet = Fernet(self.key)
        # message = fernet.decrypt(message.encode()).decode()
        return message


# if __name__ == "__main__":
#     decryption = Decryption()
#     print(decryption.decrypt(
#         "gAAAAABl6YBAOgRG5MQdk6-nKWphlu69_Dj5sIx6J0Wf4LxnN0WPg-XEJ2_WkH0mpkKCiPuCD_5PxrOSWfqdZkJw7bkw_NXZvA=="))
