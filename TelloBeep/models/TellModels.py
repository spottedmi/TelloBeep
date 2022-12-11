from TelloBeep.censorship import Censorship
from TelloBeep.config import conf
from datetime import datetime
import time

class Tells_Utills():

	def __init__(self, tellJSON):

		# self.title = title
		self.send = False
		self.metadata = self

		self.id = tellJSON["id"]
		
		self.tell = None
		# self.text = self.tell

		self.users_ip = tellJSON.get("users_ip") if tellJSON.get("users_ip") else "0.0.0.0" 

		# self.flag = False

		
		

		self.filename = None


	def get_date(self, tellJSON):
		try:
			d = datetime.strptime(tellJSON, "%Y-%m-%dT%H:%M:%S.000Z")
			d = d.replace(hour=time.localtime().tm_hour)
		except:
			pass
		try:	
			d = datetime.strptime(tellJSON, "%Y-%m-%dT%H:%M:%S.%f")
			d = d.replace(hour=time.localtime().tm_hour)
		except:
			pass

		return d.strftime(format="%Y-%m-%dT%H:%M:%S.000Z")

	def get_title(self, datetime):
			tm , date = datetime.rsplit("T")
			y, M, d = tm.rsplit("-")
			if len(M) == 1: M = f"0{M}"
			date, mil = date.rsplit(".")
			
			h,m,s = date.rsplit(":")

			if len(h) == 1: h = f"0{h}"
			if len(m) == 1: m = f"0{m}"
			if len(s) == 1: s = f"0{s}"
	
			if h == 24:
				conf['logger'].info(f"24 hour detected")
				h = "00"

			title = f"{y}{M}{d}{h}{m}{s}_{self.id}"
			print(title)
			return title

	def __str__(self):
		return self.tell


class Questionmi_tell(Tells_Utills):
	def __init__(self, tellJSON):
		super().__init__(tellJSON)

		self.tell = tellJSON["text"]
		# self.created_at = tellJSON["created_at"]
		# self.users_ip = tellJSON["users_ip"]
		# conf['user']s_fingerprint = tellJSON["users_fp"]
		
		self.created_at = self.get_date(tellJSON["created_at"])
		self.title = self.get_title(self.created_at)

		

		self.cen = Censorship()
		self.cen.TEXT = self.tell
		self.flag  = self.cen.flag_word()


		


class Tellonym_tell(Tells_Utills):
	def __init__(self, tellJSON):
		super().__init__(tellJSON)

		self.tell = tellJSON["tell"]
		# self.users_ip = "0.0.0.0"

		# self.flag = False

		self.created_at = self.get_date(tellJSON["createdAt"])
		self.title = self.get_title(self.created_at)

		
		self.cen = Censorship()
		self.cen.TEXT = self.tell
		self.flag  = self.cen.flag_word()





class Questionmi_user():
	def __init__(self, tokenJSON):		
		user_id = tokenJSON["userId"]
		self.token = tokenJSON["accessToken"]


class Tellonym_user():
	def __init__(self, tokenJSON):
		user_id = tokenJSON["userId"]
		self.token = tokenJSON["accessToken"]

		