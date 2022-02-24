import clients

"""
With this client, we checking the server.
Run it from the command line.
first, run the serverTask.py file
and then run the client.py file
"""

URL = 'http://localhost:5000'

client = clients.Client(URL)


# This class if for encrypting and decrypting messages.
class EncryptDecryptMessage:
    # This method will encrypt a message that the user inputted.
    # The method will print a message ID and a key so the user will be able to decrypt his/hers message.
    # The user must copy the key and save it somewhere safe so he/she will be able to decrypt the message.
    def encrypt_message(self, message):
        new_message = {'message': message}
        request = client.post('/newmessages', data=new_message)
        data = request.json()
        print("-------------------------------------------")
        print("Your message ID is: ", data[0])
        print("Your key is: ", data[1])
        print("-------------------------------------------\n")
        print("Please save your message ID and key safely")
        print("-------------------------------------------\n")
        # self.decrypt_message(data[0], data[1])

    # This method will decrypt a message with a message ID and a key.
    # The method will print the decrypted message.
    def decrypt_message(self, message_id, key):
        request = client.post('/decrypt', data={'message': message_id, 'key': key})
        data = request.json()
        print("-------------------------------------------")
        print(data)
        print("-------------------------------------------\n")

    # This method checks if the input (action choice or message ID) is an integer
    def check_user_input(self, Users_integer_input):
        try:
            # try to convert the user input into integer
            int(Users_integer_input)
            return True
        except ValueError:
            return False

    # In this method, we get input from the user and And operate the other methods
    def users_input(self):
        flag = 1
        while flag:
            print("Please choose: \n" "1 to encrypt a message \n" "2 to decrypt a message \n" "3 to exit \n")
            choice = input("Would you like to encrypt, decrypt or exit : ")
            if self.check_user_input(choice):

                if choice == '1':
                    message = input("Input your message here: ")
                    if not message:
                        print("-------------------------------------------")
                        print("Message can't be empty")
                    else:
                        self.encrypt_message(message)
                    print("-------------------------------------------")

                elif choice == '2':
                    message_id = input("Input your message ID: ")
                    if self.check_user_input(message_id):
                        key = input("Input your key: ")
                        self.decrypt_message(message_id, key)
                    else:
                        print("-------------------------------------------")
                        print("Input is not a number. Try again")
                        print("-------------------------------------------")

                elif choice == '3':
                    flag = 0

            else:
                print("-------------------------------------------")
                print("Input is not a number. Try again")
                print("-------------------------------------------")


secret = EncryptDecryptMessage()
secret.users_input()
