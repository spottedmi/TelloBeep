import requests, json, sys, time
from queue import Queue
import importlib
from models.TellModels import Questionmi_user, Questionmi_tell

from config import conf
from discord.notifications import Notify


from exceptions.exceptions import TokenInvalidQuestionmi, ConnectionTimeout, CaptchaRequired






class Questionmi_api():
	q_list = None
	def __init__(self, q_list=None):
		
		

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
				conf['logger'].error(f"cannot load token")

				time.sleep(loop)
				loop += loop
				raise e
				# return False


			if conf['user']:
				try:
					self.get_tells(conf['user'].token)
					# conf['logger'].info(f"tells fetched")

					break

				except ConnectionTimeout as e:
					# conf['logger'].error(f"connection timeout")
					print("conneciton timeout")
					time.sleep(loop)
					loop += loop
					raise Exception("xD") from None

				except TokenInvalidQuestionmi as e:
					print("questionmi token invalid")
					conf['logger'].error(f"questionmi  token invalid")

					# try:
					# 	self.get_token()
					# 	break

					# except CaptchaRequired:
					# 	print("captcha required")
					# 	conf['logger'].error(f"captcha required")

					# 	time.sleep(loop)
					# 	loop += loop

	

		# for elem in conf['tells']:
			# self.remove_tell(elem.id)

			
			
		# self.load_locals()

		
		return conf['tells']


	# def get_login_credentials(self):

	# 	Notify(q_list=self.q_list, error="TELLO_RELOGIN")
	# 	conf['logger'].error(f"tellonym relogin")

	# 	if not conf['LOGIN_TELLONYM'] and not conf['PASSWORD_TELLONYM']:
	# 		conf['LOGIN_TELLONYM'] = input("login: ")
	# 		conf['PASSWORD_TELLONYM'] = input("password: ")


	def load_token(self, file=None):
		# use pre-defined file location
		"load token from file"

		file = conf['token_questionmi']
		
		if file == "" or file == None:
			raise TokenInvalidQuestionmi(q_list=self.q_list)

		res  = {
			"userId" : "2137",
			"accessToken": file
			}

		conf['user'] = Questionmi_user(res)

	
		# try:
		# 	with open(file, "r") as f:
		# 		res = f.read()
		# 	res = json.loads(res)

			
		# 	conf['user'] = Tellonym_user(res)

		# except Exception as e:
		# 	# return conf['ERRORS'].get("load_token")
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
	# 		"email": conf['LOGIN_TELLONYM'],
	# 		"password": conf['PASSWORD_TELLONYM'],
	# 		"limit": "25"
	# 	}

	# 	headers = conf['headers']
	# 	conf['headers']["Content-Length"] = f"{len(str(data_login))}"

	# 	response = requests.post(url, headers=headers, json=data_login, timeout=5000)

	# 	data = response.json()

	# 	close = False

	# 	if data.get("code") == conf['ERRORS'].get("captcha"):
	# 		raise CaptchaRequired(q_list=self.q_list)
	# 		# Notify(q_list=self.q_list, error="CAPTCHA_REQUIRED")
	# 		# return conf['ERRORS'].get("captcha")
	# 	else: 
	# 		conf['user'] = Questionmi_user(data)
	# 		self.save_token(data=data)
				
	# 	if close:
	# 		sys.exit(0)
		

	def remove_tell(self, tell_id, limit=25):
		url = f"{conf['questionmi_api_base_url']}Tells"
		payload = {
				"id": tell_id,
				}
		headers = {}
		headers["token"] = f"{conf['user'].token}"
		conf['logger'].info(f"remove fetched tells")


		r = requests.delete(url, headers=headers, params=payload)
		
		return r


	def get_tells(self, token=""):
		# importlib.reload(requests)
		conf['tells'] = list()
		# url = f"{conf['questionmi_api_base_url']}Tells"
		url = f"{conf['questionmi_api_base_url']}GetTellsForPost"

		headers = {}
		headers["token"] = f"{conf['user'].token}"

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
			conf['logger'].error(f"questionmi get tells failed")

			x = response.json()["err"]
			x = x["code"]
			conf['logger'].error(f"error: {x}" )


			if x == conf['ERRORS'].get("token"):
				raise TokenInvalidQuestionmi
			return x

		for x in data:		
		
			# cen = Censorship()
			# cen.TEXT = x["tell"]
			# FLAG = cen.flag_word()
			tell = Questionmi_tell(x)
			# tell.flag = FLAG
			# print(f"parsed tell: {tell}")
			
			conf['tells'].append(tell)
			# self.remove_tell(tell_id=tell.id)

		return conf['tells']





if __name__ == "__main__":
	tell = Questionmi_api()
	out = tell.run()

	if out == list():
		print("no tells")
	for elem in out :
		print(f"{elem.id}  {elem.created_at}  {elem.tell} {elem.user_ip}")



