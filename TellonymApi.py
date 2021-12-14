import requests, json, sys, time
from queue import Queue
from threading import Thread
import importlib

from config import Config
from censorship import Censorship

from notifications import Notify

from exceptions import TokenInvalid, ConnectionTimeout



class Tellonym_user():
	def __init__(self, tokenJSON):
		self.user_id = tokenJSON["userId"]
		self.token = tokenJSON["accessToken"]

class Tellonym_tell():
	def __init__(self, tellJSON):
		self.id = tellJSON["id"]
		self.tell = tellJSON["tell"]
		self.created_at = tellJSON["createdAt"]
		self.flag = False

class Tellonym_api(Config):
	q_list = None
	def __init__(self, q_list=None):
		super().__init__()
		if q_list != None:
			self.q_list = q_list

	ERROR = False

	def run(self):
		#self.get_token()
		loop = 5
		try:
			self.load_token()
			# self.check_err(tls)

		except TokenReadImpossible:
			print("cannot read a token")
			time.sleep(loop)
			loop += loop


		if self.user:
			# tls = self.get_tells(self.user.token)
			# self.check_err(tls)
			try:
				self.get_tells(self.user.token)

			except ConnectionTimeout:
				print("conneciton timeout")
				time.sleep(loop)
				loop += loop

			except TokenInvalid:
				print("token invalid")
				self.get_token()


			
		
		# if self.ERROR == self.ERRORS.get("token"):
		# 	try:

		# 		tls = self.get_token()


		# 		if tls:

		# 			self.check_err(tls)
		# 	except Exception as e:

		# 		self.ERROR = self.ERRORS.get("load_token")

		# if self.ERROR:
		# 	return self.ERROR
	

		for elem in self.tells:
			self.remove_tell(elem.id)
			
		# self.load_locals()

		
		return self.tells


	def get_login_credentials(self):

		Notify(q_list=self.q_list, error="TELLO_RELOGIN")
		if not self.LOGIN_TELLONYM and not self.PASSWORD_TELLONYM:
			self.LOGIN_TELLONYM = input("login: ")
			self.PASSWORD_TELLONYM = input("password: ")


	def load_token(self, file=None):
		# use pre-defined file location
		"load token from file"
		file = self.token_file
		try:
			with open(file, "r") as f:
				res = f.read()
			res = json.loads(res)

			
			self.user = Tellonym_user(res)

		except Exception as e:
			# return self.ERRORS.get("load_token")
			raise TokenInvalid(q_list=self.q_list)
		return True

	def save_token(self, file=None, data=""):
		"save token to a file"
		file = file if file  else self.token_file
		with open(file, "w+") as f:
			f.write(json.dumps(data))

	def get_token(self):
		url = "https://api.tellonym.me/tokens/create"

		self.get_login_credentials()


		data_login = {
			"deviceName": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.11",
			"deviceType": "web",
			"lang": "en",
			"captcha": "",#m3gon
			"email": self.LOGIN_TELLONYM,
			"password": self.PASSWORD_TELLONYM,
			"limit": "25"
		}

		headers = self.headers
		self.headers["Content-Length"] = f"{len(str(data_login))}"

		response = requests.post(url, headers=headers, json=data_login, timeout=5000)

		data = response.json()

		close = False

		if data.get("code") == self.ERRORS.get("captcha"):
			Notify(q_list=self.q_list, error="CAPTCHA_REQUIRED")
			return self.ERRORS.get("captcha")
		else: 
			self.user = Tellonym_user(data)
			self.save_token(data=data)
		
		if close:
			sys.exit(0)
		

	def remove_tell(self, tell_id, limit=25):
		url = f"https://api.tellonym.me/"
		url = url + "tells/destroy"
		data = {
				"tellId": tell_id,
				"limit": limit,
				}
		headers = self.headers
		headers["authorization"] = f"Bearer {self.user.token}"

		r = requests.post(url, json=data, headers=headers)
		return r.content


	def get_tells(self, token=""):
		importlib.reload(requests)
		self.tells = list()
		url = "https://api.tellonym.me/tells"
		headers = self.headers
		headers["authorization"] = f"Bearer {self.user.token}"

		params = {
			"limit": "25"
		}
		try:
			time.sleep(0.01)

			response = requests.get(url, headers=headers, params=params)
		except:
			raise ConnectionTimeout( q_list=self.q_list)
			# return self.ERRORS.get("conn_timeout")

		if response.ok:
			data = response.json()
		else:
			x = response.json()["err"]
			x = x["code"]


			return x

		for x in data["tells"]:		
			cen = Censorship()
			cen.TEXT = x["tell"]
			FLAG = cen.flag_word()
			tell = Tellonym_tell(x)
			tell.flag = FLAG
			
			
			self.tells.append(tell)
			# self.remove_tell(token, tell.id)

		return self.tells


if __name__ == "__main__":
	tell = Tellonym_api()
	out = tell.run()

	if out == list():
		print("no tells")
	for elem in out :
		print(f"{elem.id}  {elem.created_at}  {elem.tell}")
