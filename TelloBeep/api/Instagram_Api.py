from instagrapi import Client
from TelloBeep.notify import Notify


from TelloBeep.config import conf
from TelloBeep.logs.logger import logger

from TelloBeep.email.email_fetcher import Mail_fetcher

import time, subprocess

class Instagram_api():
	bot = None
	q_list=None
	def __init__(self, q_list=None):
		self.logger = logger(name=__name__)
		
		if q_list != None:
			self.q_list = q_list



	def login(self):
		self.bot = Client()
		try:
			self.bot.load_settings(conf["INSTAGRAM_SESSION"])
			self.logger.info(f"logged from file, soft login")
			Notify(q_list=self.q_list, error="INSTAGRAM_LOGGED")

			return self.bot

		except FileNotFoundError:
			self.logger.warning(f"could not log from file, hard login")
			pass

		

		if conf['LOGIN_INSTAGRAM'] != "" and conf['PASSWORD_INSTAGRAM'] != "":
			sl = 5
			while 1:
				is_auth = False
				try:                    
					is_auth = self.bot.login(conf['LOGIN_INSTAGRAM'], conf['PASSWORD_INSTAGRAM'])
					self.logger.info(f"instagram logged")
					self.bot.dump_settings(conf["INSTAGRAM_SESSION"])
					self.logger.info(f"session dumped")
					break
				
				except Exception as e:
					self.logger.warning(f"instagram login error: {e}")
					if str(e) == "EOF when reading a line":
						# e = Mail_fetcher()
						# code = e.get_code()
						# is_auth = self.bot.login(conf['LOGIN_INSTAGRAM'], conf['PASSWORD_INSTAGRAM'], verification_code=code)
						
						is_auth = Bypass_email()
						self.bot.load_settings(conf["INSTAGRAM_SESSION"])

					if is_auth  == True:
						break
				
				self.logger.info(f"putting instagram to sleep: {sl} seconds")
				time.sleep(sl)
				sl = sl*2

			print("bot logged")
			Notify(q_list=self.q_list, error="INSTAGRAM_LOGGED")
		else:
			Notify(q_list=self.q_list, error="INSTAGRAM_LOGIN_SKIPPED")
			print("bot login skipped")

		return self.bot

	def upload_post(self, img_path, caption=""):
		self.logger.info(f"post uploaded. {img_path}")

		self.bot.photo_upload(
			img_path, 
			caption=caption
		)

	def upload_album(self, imgs_paths, caption=""):
		self.logger.info(f"instagram album loaded, {imgs_paths}")

		self.bot.album_upload(
			imgs_paths,
			caption = caption
		)



class Bypass_email():
	def __init__(self):
		self.logger = logger(name = __name__)

		self.p_comm = f'''
from instagrapi import Client\n
cl = Client()\n
i = cl.login("{conf['LOGIN_INSTAGRAM']}","{conf['PASSWORD_INSTAGRAM']}")\n
cl.dump_settings({conf['INSTAGRAM_SESSION']})\n
print(f"logged to the instagram account:"+ i)\n
'''
		self.command = f'''python -c '{com}'  '''

	def run_process(self):
		self.logger.info("running process")
		self.process = subprocess.Popen(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
		return process

	def check_process(self):
		self.run_process()

		while True:
			output = self.process.stdout.readline()
			out = output.decode("utf-8")
			print(out)
			self.logger.debug(f"process output: {out}")
			if "logged to the instagram account: True" in out:
				self.logger.debug(f"process output: {out}")
				break
				return True
			else:
				# code = input("CODE: ")
				e = Mail_fetcher()
				code = e.get_code()

				self.process.stdin.write(f"{code}\n".encode())
				self.process.stdin.flush()  
				output, error = self.process.communicate()

			time.sleep(1)




if __name__  == "__main__":
	path = ""
	insta = Instagram_api()
	insta.login()
	insta.upload_post(img_path=path, caption="hello world 2")


