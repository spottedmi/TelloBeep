import requests, json, sys

class TokenInvalid(Exception):
	pass

class Tellonym_user():
	def __init__(self, tokenJSON):
		self.user_id = tokenJSON["userId"]
		self.token = tokenJSON["accessToken"]

class Tellonym_tell():
	def __init__(self, tellJSON):
		self.id = tellJSON["id"]
		self.tell = tellJSON["tell"]
		self.created_at = tellJSON["createdAt"]

class Tellonym_api():

	user = None
	tells = []
	token_file = "token.txt"

	LOGIN = None
	PASSWORD = None


	headers = {
		    'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		    'content-type': 'application/json;charset=utf-8',
		    'Host': 'api.tellonym.me',
		    'Origin': 'https://tellonym.me',
		    'Sec-Fetch-Dest': 'empty',
		    'Sec-Fetch-Mode': 'cors',
		    'Sec-Fetch-Site': 'same-site',
		    'Sec-GPC': '1',
		    'TE': 'trailers',
		    'tellonym-client': 'web:0.59.4',
		    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
		}

	def __init__(self):
		#self.get_token()
		try:
			self.load_token()
			tells = self.get_tells(self.user.token)
			# print(tells)
		except TokenInvalid:
			self.get_token()
			tells = self.get_tells(self.user.token)

		print("\n"*4)
		for elem in tells:
			print(f"{elem.id}  {elem.created_at}  {elem.tell}  ")


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
		# data = json.loads(response.text)
		data = response.json()
		# print(data)

		try:
			if data["code"] == "CAPTCHA_REQUIRED":
				print("COŚ SIĘ ZEPSUŁO I NIE BYŁO MNIE SŁYCHAĆ")
				sys.exit(0)
		except: 
			self.user = Tellonym_user(data)
			self.save_token(data=data)


		
		return self.user
	
	


	def remove_tell(self, token, tellId):
		url = "https://api.tellonym.me/tells/destroy"
		headers = self.headers
		headers["authorization"] = f"Bearer {token}"

		params = {
			"tellId": tellId,
            "limit": "25"
		}

		response = requests.post(url, headers=headers, params=params)

	def get_tells(self, token=""):
		url = "https://api.tellonym.me/tells"

		headers = self.headers
		headers["authorization"] = f"Bearer {token}"


		params = {
            "limit": "25"
		}
		response = requests.get(url, headers=headers, params=params)


		
		if response.ok:
			data = response.json()
		else:
			raise TokenInvalid

		for x in data["tells"]:
			tell = Tellonym_tell(x)
			self.tells.append(tell)
			# self.remove_tell(token, tell.id)

		return self.tells


if __name__ == "__main__":
	tell = Tellonym_api()
	# token = tell.get_token()
	# print(token.token)

	# tells = tell.get_tells(token.token)
	# for elem in tells:
	# 	print(f"{elem.id}   {elem.tell}")