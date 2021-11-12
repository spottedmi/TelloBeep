import requests, json

class TellonymUser():
	def __init__(self, tokenJSON):
		self.userId = tokenJSON["userId"]
		self.token = tokenJSON["accessToken"]

class TellonymTell():
	def __init__(self, tellJSON):
		self.id = tellJSON["id"]
		self.tell = tellJSON["tell"]
		self.createdAt = tellJSON["createdAt"]

class TellonymApi():
	def GetToken(self):
		url = "https://api.tellonym.me/tokens/create"

		data_login = {
            "deviceName": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.11",
            "deviceType": "web",
            "lang": "en",
            "captcha": "",#m3gon
            "email": "spotted_kasprzak_auto",
            "password": "8f79akZ6",
            "limit": "25"
		}

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
		    'Content-Length': f"{len(str(data_login))}",
		    'Accept': 'application/json'
		}

		response = requests.post(url, headers=headers, json=data_login, timeout=5000)
		data = json.loads(response.text)

		user = TellonymUser(data)

		return user

	def RemoveTell(self, token, tellId):
		url = "https://api.tellonym.me/tells/destroy"

		headers = {
		  'Accept': 'application/json',
		  'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		  'Connection': 'keep-alive',
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
		  'authorization': 'Bearer {}'.format(token)
		}

		params = {
			"tellId": tellId,
            "limit": "25"
		}

		response = requests.post(url, headers=headers, params=params)

	def GetTells(self, token):
		url = "https://api.tellonym.me/tells?limit=25"

		headers = {
		  'Accept': 'application/json',
		  'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		  'Connection': 'keep-alive',
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
		  'authorization': 'Bearer {}'.format(token)
		}

		response = requests.get(url, headers=headers)
		data = json.loads(response.text)

		tells = []

		for x in data["tells"]:
			tell = TellonymTell(x)

			tells.append(tell)
			self.RemoveTell(token, tell.id)

		return tells