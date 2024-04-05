import os
from dotenv import load_dotenv


class Decryption:
    def __init__(self):
        load_dotenv()
        key = os.getenv('KEY')
        self.n, self.d = [int(x, 16) for x in key.split(',')]

    def decrypt(self, encrypted_message):
        # separate by %2C
        encrypted_message = encrypted_message.split('%2C')
        print(encrypted_message)
        decrypted_message = []
        for i in encrypted_message:
            i = int(i)
            decrypted_message.append(chr(pow(i, self.d, self.n)))

        return ''.join(decrypted_message)
        # return encrypted_message


# if __name__ == "__main__":
#     decryption = Decryption()
#     print(decryption.decrypt("82797263122673622252398609254816336932239895641311134141567714134294435441920468572069431727612875451590765722563750610444743739647654043451189443008711099411881516504023383958426332148078113117728534264956495158706799921811190059563764862096717623117364576125108214657489794083908300707317521383930137922526"))
