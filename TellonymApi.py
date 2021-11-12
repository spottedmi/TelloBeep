import requests
import json

class TellonymTell():
	def __init__(self, tellJSON):
		self.id = tellJSON["id"]
		self.tell = tellJSON["tell"]
		self.createdAt = tellJSON["createdAt"]

class TellonymApi():
	def RemoveTell(self, tellId):
		print('delete ' + str(tellId))

	def GetTells(self, token):
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

		request = requests.get("https://api.tellonym.me/tells?limit=25", headers=headers)
		data = json.loads(request.text)

		tells = []

		for x in data["tells"]:
			tell = TellonymTell(x)

			tells.append(tell)
			self.RemoveTell(tell.id)

		return tells
