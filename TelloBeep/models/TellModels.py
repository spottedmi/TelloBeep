from TelloBeep.censorship import Censorship
from TelloBeep.config import conf
from datetime import datetime
import time

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
		self.created_at = self.get_date(tellJSON["createdAt"])
		self.users_ip = "0.0.0.0"

		self.flag = False

	def get_date(self, tellJSON):
		d = datetime.strptime(tellJSON, "%Y-%m-%dT%H:%M:%S.000Z")
		d = d.replace(hour=time.localtime().tm_hour)

		return d.strftime(format="%Y-%m-%dT%H:%M:%S.000Z")