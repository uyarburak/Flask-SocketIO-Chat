users = {}

def addUser(name, hashed_password):
	if name in users:
		raise NameError('There is already a user with the same name')
	user = {"name" : name, "password" : hashed_password, "token" : "null", "challenge" : "null"}
	users[name] = user

def getUser(name):
	if name not in users:
		raise NameError('User not found')
	return users[name]

def initForDemo():
	# "7c4a8d09ca3762af61e59520943dc26494f8941b" is the SHA1 of "123456" in base 16.
	addUser("user1", "7c4a8d09ca3762af61e59520943dc26494f8941b")
	addUser("user2", "7c4a8d09ca3762af61e59520943dc26494f8941b")
	addUser("user3", "7c4a8d09ca3762af61e59520943dc26494f8941b")
	addUser("user4", "7c4a8d09ca3762af61e59520943dc26494f8941b")