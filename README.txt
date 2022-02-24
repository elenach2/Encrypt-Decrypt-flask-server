*** General purpose: 
	Rest api web server with encrypt/ decrypt messages service.
	When a message is inputted the server encrypts it and returns to the client a "message ID" and  "key". 
	With the given key and message ID the message can be decrypted.
	
*** Installation: 
	pip install flask
	pip install flask-restful
	pip install requests
	pip install client

*** How to run the script:
	Open command line (cmd) 
	Commands to run in the command line:
		Run severTask.py
		Run client.py

***To do in the cmd after you run the client.py
	choose: 
		1 to encrypt a message 
			input: message
			output: message id and key
		2 to decrypt a message 
			input: message id and key
			output: decrypted message
		3 to exit
			exits the program.

		