import os
from dotenv import load_dotenv


class Decryption:
    def __init__(self):
        load_dotenv()
        key = os.getenv('KEY')
        self.n, self.d = [int(x, 16) for x in key.split(',')]

    def decrypt(self, encrypted_message):
        # TODO remove comments and return when done testing
        encrypted_message = [encrypted_message]
        decrypted_message = [chr(pow(char, self.d, self.n)) for char in encrypted_message]
        return ''.join(decrypted_message)
        # return encrypted_message


if __name__ == "__main__":
    decryption = Decryption()
    print(decryption.decrypt(3931946207050845389613283327554538059130452635054030560366918972713655765235634179403788805931045307253404522531524182458929899383354584013253351837339141113181187478507027021631004459756582607400756809078244794981441783884766057823141242374969734608334111960568365416050055475626082131581947173752574833575))
