import os
from dotenv import load_dotenv
import jwt


class Decryption:
    def __init__(self):
        load_dotenv()
        self.key = os.getenv('KEY')

    def decrypt(self, encrypted_message):
        # decrypt the data using the key
        decode = jwt.decode(encrypted_message, self.key, algorithms=['HS256'])
        return decode


# if __name__ == "__main__":
#     decryption = Decryption()
#     print(decryption.decrypt("82797263122673622252398609254816336932239895641311134141567714134294435441920468572069431727612875451590765722563750610444743739647654043451189443008711099411881516504023383958426332148078113117728534264956495158706799921811190059563764862096717623117364576125108214657489794083908300707317521383930137922526"))
