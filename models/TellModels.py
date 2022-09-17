from censorship.censorship import Censorship
class Questionmi_user():
	def __init__(self, tokenJSON):		
		user_id = tokenJSON["userId"]
		self.token = tokenJSON["accessToken"]

class Questionmi_tell():
	def __init__(self, tellJSON):

		self.id = tellJSON["id"]
		self.tell = tellJSON["text"]
		self.created_at = tellJSON["created_at"]
		self.users_ip = tellJSON["users_ip"]
		# conf['user']s_fingerprint = tellJSON["users_fp"]
		

		self.cen = Censorship()
		self.cen.TEXT = self.tell
		self.flag  = self.cen.flag_word()


class Tellonym_user():
	def __init__(self, tokenJSON):
		user_id = tokenJSON["userId"]
		self.token = tokenJSON["accessToken"]

class Tellonym_tell():
	def __init__(self, tellJSON):
		self.id = tellJSON["id"]
		self.tell = tellJSON["tell"]
		self.created_at = tellJSON["createdAt"]
		self.flag = False