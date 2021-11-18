import requests, json, sys
from queue import Queue
from threading import Thread

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


	def run(self):
		#self.get_token()
		try:
			self.load_token()
			tells = self.get_tells(self.user.token)
		except TokenInvalid:
			self.get_token()
			tells = self.get_tells(self.user.token)

		for elem in tells:
			self.remove_tell(elem.id)

		return tells


	def get_login_credentials(self):
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
		except:
			print("load json failed")
			raise TokenInvalid

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

		try:
			if data["code"] == "CAPTCHA_REQUIRED":
				print("COŚ SIĘ ZEPSUŁO I NIE BYŁO MNIE SŁYCHAĆ")
				sys.exit(0)
		except: 
			self.user = Tellonym_user(data)
			self.save_token(data=data)


		
		return self.user

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
		self.tells = list()
		url = "https://api.tellonym.me/tells"
		headers = self.headers
		headers["authorization"] = f"Bearer {self.user.token}"


		params = {
			"limit": "25"
		}
		
		response = requests.get(url, headers=headers, params=params)
		if response.ok:
			data = response.json()
		else:
			raise TokenInvalid(response.text)
		for x in data["tells"]:
			tell = Tellonym_tell(x)
			self.tells.append(tell)
			# self.remove_tell(token, tell.id)

		return self.tells


if __name__ == "__main__":
	tell = Tellonym_api()
	out = tell.run()
	print("fetched tells: ")
	if out == list():
		print("no tells")
	for elem in out :
		print(f"{elem.id}  {elem.created_at}  {elem.tell}")