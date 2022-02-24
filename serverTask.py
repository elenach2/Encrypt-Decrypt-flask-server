from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from cryptography.fernet import Fernet
import json

"""
Rest api web server with encrypt/ decrypt messages service.
When a message is inputted the server encrypts it and returns to the client a "message ID" and  "key". 
With the given key and message ID the message can be decrypted.

Commands to run in the command line:

To see all the encrypted messages:
    curl http://localhost:5000/messages/all
    
To see a specific encrypted message:
    curl http://localhost:5000/messages/<message_id>
    
To add a new message:
    curl http://localhost:5000/newmessages -d "message=<user_message>" -X POST
    
To decrypt a message:
    curl http://localhost:5000/decrypt -d "message=<message_id>&key=<users_key>" -X POST
    
"""

app = Flask("SecretMessageAPI")
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('message', required=False)
parser.add_argument('key', required=False)


messages = {}


# Create a json file to save the data
def write_changes_to_file():
    global messages
    with open('messages.json', 'w') as f:
        json.dump(messages, f)


# If json already exists, use it if not create the json.
try:
    with open('messages.json', 'r') as f:
        messages = json.load(f)

except IOError:
    write_changes_to_file()


# Through this the class "SecretMessages" we can see all the encrypted messages or to see a specific encrypted message
class SecretMessages(Resource):

    def get(self, message_id):
        if message_id == "all":
            return messages
        if message_id not in messages:
            abort(404, message=f"message {message_id} not found")
        return messages[message_id]


# The class "NewMessage" let us get a new message and to encrypt it before it saves it
class NewMessage(Resource):
    # in the init we get a new secret key for every message the user inputs.
    def __init__(self):
        super().__init__()
        self.key = Fernet.generate_key()

    # the post method gets the message, encrypts it and saves it
    def post(self):
        args = parser.parse_args()
        if len(messages) == 0:
            new_message = {'message': args['message']}
            message_id = 1
        else:
            new_message = {'message': args['message']}
            # The messages ID constantly increases by one according to the number of messages
            message_id = str(max(int(m) for m in messages.keys()) + 1)

        
        messages[message_id] = self.encrypt_message(new_message['message'])
        # For us to send a key to the user we need to change its type to string for bytes.
        output_for_the_client = [message_id, self.key.decode('utf8')]
        write_changes_to_file()
        return output_for_the_client, 201

    # This method encrypts the message.
    def encrypt_message(self, msg):
        f = Fernet(self.key)
        token = f.encrypt(str.encode(msg))
        return token.decode('utf8')


# With the class "DecryptGivenMessage", we decrypting the secret message with the secret key.
class DecryptGivenMessage(Resource):
    # The post method finds the message ID in the json file and
    # sends the encrypted message to the "decrypt_message" method
    def post(self):
        if len(messages) == 0:
            return "___ NO MESSAGES TO DECRYPT ___"
        client_input = parser.parse_args()
        if client_input["message"] not in messages.keys():
            msg = client_input["message"]
            abort(400, message=f"message {msg} not found")
            return
        else:
            # For us to send a message and a ket to the "decrypt_message" method
            # we need to change its type to bytes.
            message = self.decrypt_message(messages[client_input["message"]], client_input["key"])
            return message, 201

    # This method decrypts the message.
    def decrypt_message(self, encrypted_msg, key):
        key = key.encode('utf8')
        encrypted_msg = encrypted_msg.encode('utf8')

        try:
            f = Fernet(key)
            msg = f.decrypt(encrypted_msg)
            print(msg)
            return msg.decode('utf8')

        except:
            return "___WRONG INPUT___"


api.add_resource(SecretMessages, '/messages/<message_id>')
api.add_resource(NewMessage, '/newmessages')
api.add_resource(DecryptGivenMessage, '/decrypt')

if __name__ == '__main__':
    app.run()
