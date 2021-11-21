import requests, json, sys, time
from queue import Queue
from threading import Thread
import importlib

from config import Config

class TokenInvalid(Exception):
	def __init__(self, err=""):
		print("___token invalid___")
		print(err)


class Tellonym_user():
	def __init__(self, tokenJSON):
		self.user_id = tokenJSON["userId"]
		self.token = tokenJSON["accessToken"]

class Tellonym_tell():
	def __init__(self, tellJSON):
		self.id = tellJSON["id"]
		self.tell = tellJSON["tell"]
		self.created_at = tellJSON["createdAt"]

class Tellonym_api(Config):

	ERROR = False

	def run(self):
		#self.get_token()
		print("run")
		tls = self.load_token()
		self.check_err(tls)
		if self.user:
			tls = self.get_tells(self.user.token)
			self.check_err(tls)
		
		if self.ERROR == self.ERRORS.get("token"):
			tls = self.get_token()
			if tls:
				print(f" get token {tls}")
				self.check_err(tls)

		if self.ERROR:
			return self.ERROR
	

		for elem in self.tells:
			self.remove_tell(elem.id)
		
		return self.tells


	def get_login_credentials(self):
		print("Using credentials")
		if not self.LOGIN and not self.PASSWORD:
			self.LOGIN = input("login: ")
			self.PASSWORD = input("password: ")


	def load_token(self, file=None):
		# use pre-defined file location
		"load token from file"
		file = file if file  else self.token_file
		try:
			with open(file, "r") as f:
				res = f.read()
			res = json.loads(res)
			
			self.user = Tellonym_user(res)
		except Exception as e:
			print(e)
			print("load json failed")
			return self.ERRORS.get("load_token")
			# raise TokenInvalid("load token failed")
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
			"email": self.LOGIN,
			"password": self.PASSWORD,
			"limit": "25"
		}

		headers = self.headers
		self.headers["Content-Length"] = f"{len(str(data_login))}"

		response = requests.post(url, headers=headers, json=data_login, timeout=5000)
		data = response.json()
		close = False

		if data.get("code") == self.ERRORS.get("captcha"):
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
			return self.ERRORS.get("conn_timeout")

		if response.ok:
			data = response.json()
		else:
			x = response.json()["err"]
			x = x["code"]
			return x

		for x in data["tells"]:
			tell = Tellonym_tell(x)
			self.tells.append(tell)
			# self.remove_tell(token, tell.id)

		return True


if __name__ == "__main__":
	tell = Tellonym_api()
	out = tell.run()
	print("fetched tells: ")
	if out == list():
		print("no tells")
	for elem in out :
		print(f"{elem.id}  {elem.created_at}  {elem.tell}")