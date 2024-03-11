import os
from dotenv import load_dotenv


class Decryption:
    def __init__(self):
        load_dotenv()
        key = os.getenv('KEY')
        self.n, self.d = [int(x, 16) for x in key.split(',')]

    def decrypt(self, encrypted_message):
        # TODO remove comments and return when done testing
        # encrypted_message = [int(encrypted_message)]
        # decrypted_message = ''.join([chr(pow(int(char), self.d, self.n)) for char in encrypted_message])
        # return decrypted_message
        return encrypted_message


# if __name__ == "__main__":
#     decryption = Decryption()
#     print(decryption.decrypt("93170485217644808136623805722300481109594233128562405997672195557014364348133205538729907885288218963258194390116096938072677469277356766691940572264211050666569665841104200554353873142299571272735198503912924779488845867606627746162096269587458429549324453991981491067555768577864224883995387039985071551313"))
