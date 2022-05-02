import requests, json, sys, time
from queue import Queue
from threading import Thread
import importlib
from TellModels import Questionmi_user, Questionmi_tell

from config import Config

from notifications import Notify

from exceptions import TokenInvalidQuestionmi, ConnectionTimeout, CaptchaRequired






class Questionmi_api(Config):
	q_list = None
	def __init__(self, q_list=None):
		super().__init__(child_class=__class__.__name__)
		if q_list != None:
			self.q_list = q_list

	ERROR = False

	def run(self):
		loop = 5
		while True:
			try:
				self.load_token()

			# except TokenReadImpossible:
			except Exception as e:
				print(f"cannot read a token {e}")
				self.logger.error(f"cannot load token")

				time.sleep(loop)
				loop += loop
				return False


			if self.user:
				try:
					self.get_tells(self.user.token)
					break

				except ConnectionTimeout as e:
					# self.logger.error(f"connection timeout")
					print("conneciton timeout")
					time.sleep(loop)
					loop += loop
					raise Exception("xD") from None

				except TokenInvalidQuestionmi as e:
					print("questionmi token invalid")
					self.logger.error(f"questionmi  token invalid")

					# try:
					# 	self.get_token()
					# 	break

					# except CaptchaRequired:
					# 	print("captcha required")
					# 	self.logger.error(f"captcha required")

					# 	time.sleep(loop)
					# 	loop += loop

	

		for elem in self.tells:
			self.remove_tell(elem.id)
			
			
		# self.load_locals()

		
		return self.tells


	# def get_login_credentials(self):

	# 	Notify(q_list=self.q_list, error="TELLO_RELOGIN")
	# 	self.logger.error(f"tellonym relogin")

	# 	if not self.LOGIN_TELLONYM and not self.PASSWORD_TELLONYM:
	# 		self.LOGIN_TELLONYM = input("login: ")
	# 		self.PASSWORD_TELLONYM = input("password: ")


	def load_token(self, file=None):
		# use pre-defined file location
		"load token from file"

		file = self.token_questionmi
		
		if file == "" or file == None:
			raise TokenInvalidQuestionmi(q_list=self.q_list)

		res  = {
			"userId" : "2137",
			"accessToken": file
			}

		self.user = Questionmi_user(res)

	
		# try:
		# 	with open(file, "r") as f:
		# 		res = f.read()
		# 	res = json.loads(res)

			
		# 	self.user = Tellonym_user(res)

		# except Exception as e:
		# 	# return self.ERRORS.get("load_token")
		# 	raise TokenInvalid(q_list=self.q_list)

		return True

	# def save_token(self, file=None, data=""):
	# 	"save token to a file"

	# 	file = file if file  else self.token_file
	# 	with open(file, "w+") as f:
	# 		f.write(json.dumps(data))

	# def get_token(self):
	# 	url = "https://api.tellonym.me/tokens/create"
	# 	self.get_login_credentials()


	# 	data_login = {
	# 		"deviceName": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.11",
	# 		"deviceType": "web",
	# 		"lang": "en",
	# 		"captcha": "",#m3gon
	# 		"email": self.LOGIN_TELLONYM,
	# 		"password": self.PASSWORD_TELLONYM,
	# 		"limit": "25"
	# 	}

	# 	headers = self.headers
	# 	self.headers["Content-Length"] = f"{len(str(data_login))}"

	# 	response = requests.post(url, headers=headers, json=data_login, timeout=5000)

	# 	data = response.json()

	# 	close = False

	# 	if data.get("code") == self.ERRORS.get("captcha"):
	# 		raise CaptchaRequired(q_list=self.q_list)
	# 		# Notify(q_list=self.q_list, error="CAPTCHA_REQUIRED")
	# 		# return self.ERRORS.get("captcha")
	# 	else: 
	# 		self.user = Questionmi_user(data)
	# 		self.save_token(data=data)
				
	# 	if close:
	# 		sys.exit(0)
		

	def remove_tell(self, tell_id, limit=25):
		url = f"{self.questionmi_api_base_url}Tells"
		payload = {
				"id": tell_id,
				}
		headers = {}
		headers["token"] = f"{self.user.token}"


		r = requests.delete(url, headers=headers, params=payload)

		return r


	def get_tells(self, token=""):
		# importlib.reload(requests)
		self.tells = list()
		url = f"{self.questionmi_api_base_url}Tells"
	
		headers = {}
		headers["token"] = f"{self.user.token}"

		params = {
			"page_id": 1,
			"records_per_page": 50
		}
		try:
			# response = requests.get(url, headers=headers, params=params)
			response = requests.get(url, headers=headers,  params=params)


		except requests.ConnectionError as e:
			raise ConnectionTimeout(q_list=self.q_list) 

		except Exception as e:
			print(e)
			raise e
		if response.ok:
			data = response.json()
		else:
			self.logger.error(f"questionmi get tells failed")

			x = response.json()["err"]
			x = x["code"]

			if x == self.ERRORS.get("token"):
				raise TokenInvalidQuestionmi
			return x

		for x in data:		
		
			# cen = Censorship()
			# cen.TEXT = x["tell"]
			# FLAG = cen.flag_word()
			tell = Questionmi_tell(x)
			# tell.flag = FLAG
			# print(f"parsed tell: {tell}")
			
			self.tells.append(tell)
			self.remove_tell(tell_id=tell.id)

		return self.tells





if __name__ == "__main__":
	tell = Questionmi_api()
	out = tell.run()

	if out == list():
		print("no tells")
	for elem in out :
		print(f"{elem.id}  {elem.created_at}  {elem.tell} {elem.user_ip}")



