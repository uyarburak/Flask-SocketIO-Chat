from .kripto import generateRandomString
users = {}

def addUser(name, hashed_password):
	if name in users:
		raise NameError('There is already a user with the same name')
	user = {"name" : name, "password" : hashed_password, "sso_token" : generateRandomString(), "challenge" : generateRandomString(), "session_key" : generateRandomString()}
	users[name] = user

def getUser(name):
	if name not in users:
		raise NameError('User not found')
	return users[name]

def getSessionKeyOfUserWithToken(name, sso_token):
	if name not in users:
		raise NameError('User not found')
	if users[name]['sso_token'] != sso_token:
		raise NameError('Token is invalid')
	return users[name]['session_key']

def initForDemo():
	# "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92" is the SHA56 of "123456" in base 16.
	addUser("user1", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92")
	addUser("user2", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92")
	addUser("user3", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92")
	addUser("user4", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92")