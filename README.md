Flask-SocketIO-Chat
===================

A simple chat application that demonstrates how to structure a Flask-SocketIO application.

To run this application install the requirements in a virtual environment
check if virtualenv is installed:
	$ virtualenv --version
if error comes up, install it:
	$ sudo apt-get install python-virtualenv
Then create a virtualenv like this:
	$ virtualenv ENV
	$ source ENV/bin/activate
	$ pip install -r requirements.txt
	$ virtualenv ENV
If anything goes wrong try this:
	$ sudo apt-get install python-dev

After requirements has installed, you can run simply:
	$ run `python chat.py` and visit `http://localhost:5000` on one or more browser tabs.
