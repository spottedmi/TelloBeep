import requests, json, sys, time
from queue import Queue
from threading import Thread
import importlib
from TelloBeep.models.TellModels import Tellonym_user, Tellonym_tell
from TelloBeep.config import conf
from TelloBeep.censorship.censorship import Censorship

from TelloBeep.notify import Notify

from TelloBeep.exceptions.exceptions import TokenInvalidTellonym, ConnectionTimeout, CaptchaRequired






class Tellonym_api():
	q_list = None
	def __init__(self, q_list=None):
		self.user = None
		self.tells = list()
		
		if q_list != None:
			self.q_list = q_list

	ERROR = False

	def run(self):
		loop = 5
		while True:
			try:
				self.load_token()

			except TokenReadImpossible:
				print("cannot read a token")
				conf['logger'].error(f"cannot load token")

				return False
				time.sleep(loop)
				loop += loop

			if self.user:
				try:
					self.get_tells()					
					break

				except ConnectionTimeout as e:
					# conf['logger'].error(f"connection timeout")
					print(f"connection timeout {e}")
					time.sleep(loop)
					loop += loop
					print(f"sleep {loop}")
					raise Exception("xD") from None

				except TokenInvalidTellonym as e:
					print("Tellonym token invalid")
					conf['logger'].error(f"Tellonym token invalid")

					try:
						self.get_token()
						break

					except CaptchaRequired:
						print("captcha required")
						conf['logger'].error(f"captcha required")

						time.sleep(loop)
						loop += loop

	

		for elem in self.tells:
			self.remove_tell(elem.id)
			
		# self.load_locals()

		
		return self.tells


	def get_login_credentials(self):

		Notify(q_list=self.q_list, error="TELLO_RELOGIN")
		conf['logger'].error(f"tellonym relogin")

		if not conf['LOGIN_TELLONYM'] and not conf['PASSWORD_TELLONYM']:
			conf['LOGIN_TELLONYM'] = input("login: ")
			conf['PASSWORD_TELLONYM'] = input("password: ")


	def load_token(self, file=None):
		# use pre-defined file location
		"load token from file"
		file = conf['token_file_tellonym']
		try:
			with open(file, "r") as f:
				res = f.read()
			res = json.loads(res)			
			self.user = Tellonym_user(res)

		except Exception as e:
			# return conf['ERRORS'].get("load_token")
			raise TokenInvalidTellonym(q_list=self.q_list)

		return True

	def save_token(self, file=None, data=""):
		"save token to a file"

		file = file if file  else conf['token_file_tellonym']
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
			"email": conf['LOGIN_TELLONYM'],
			"password": conf['PASSWORD_TELLONYM'],
			"limit": "25"
		}

		headers = conf['headers']
		conf['headers']["Content-Length"] = f"{len(str(data_login))}"

		response = requests.post(url, headers=headers, json=data_login, timeout=15)

		data = response.json()

		close = False

		if data.get("code") == conf['ERRORS'].get("captcha"):
			raise CaptchaRequired(q_list=self.q_list)
			# Notify(q_list=self.q_list, error="CAPTCHA_REQUIRED")
			# return conf['ERRORS'].get("captcha")
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
		headers = conf['headers']
		headers["authorization"] = f"Bearer {self.user.token}"

		r = requests.post(url, json=data, headers=headers)
		return r.content


	def get_tells(self):
		importlib.reload(requests)
		self.tells = list()
		url = "https://api.tellonym.me/tells"
		headers = conf['headers']
		headers["authorization"] = f"Bearer {self.user.token}"

		params = {
			"limit": "25"
		}
		try:
			response = requests.get(url, headers=headers, params=params, timeout=20 )
		except requests.ConnectionError as e:
			print(f"error {e}")
			raise ConnectionTimeout(q_list=self.q_list) 

		except Exception as e:
			print(e)
			raise e
		if response.ok:
			data = response.json()
		else:
			conf['logger'].error(f"tellonym get tells failed")

			x = response.json()["err"]
			x = x["code"]

			if x == conf['ERRORS'].get("token"):
				raise TokenInvalidTellonym
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
	print(out)

	if out == list():
		print("no tells")
	for elem in out :
		print(f"{elem.id}  {elem.created_at}  {elem.tell}")
