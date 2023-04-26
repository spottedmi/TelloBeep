
from instagrapi import Client
from instagrapi.mixins.challenge import ChallengeChoice
from TelloBeep.notify import Notify

from TelloBeep.logs.logger import logger

from TelloBeep.email.email_fetcher import Mail_fetcher
from TelloBeep.email.bypass import Bypass_email

import time, subprocess, sys




class Instagram_api():
	bot = None
	q_list=None
	def __init__(self, q_list=None, conf=None, config_class=None):
		if conf:
			self.conf = conf
		if config_class:
			self.config_class = config_class
		
		self.logger = logger(name=f"{self.conf.get('instance')}_{__name__}")
			
		self.config_class.print_xD()
		

		if q_list != None:
			self.q_list = q_list


	def change_password_handler(username):
		# Simple way to generate a random string
		chars = list("abcdefghijklmnopqrstuvwxyz1234567890!&£@#")
		password = "".join(random.sample(chars, 15))
		self.logger.warning(f"password changing, new password: {password[0]}****{password[-1]}")
		Notify(q_list=self.q_list, error=f"password changing, new password: {password[0]}****{password[-1]}")
		self.conf["LOGIN_INSTAGRAM"] = password
		self.config_class.dump_json()

		return password

	def challenge_code_handler(username, choice):
		if choice == ChallengeChoice.SMS:
			self.logger.warning(f"challange code handler, sms called")
			Notify(q_list=self.q_list, error=f"challange code handler, sms called")			
			
			return False

		elif choice == ChallengeChoice.EMAIL:
			code = Mail_fetcher().get_code()
			
			self.logger.warning(f"challange code handler, email code: {code[0]}****{code[-1]}")
			Notify(q_list=self.q_list, error=f"challange code handler, email code: {code[0]}****{code[-1]}")			
			
			return code
		
		return False


	def login(self, hard_login=False):
		self.bot = Client()
		# self.bot.challenge_code_handler = self.challenge_code_handler
		# self.bot.change_password_handler = self.change_password_handler

		if hard_login == False:	
			try:
				self.bot.load_settings(self.conf["INSTAGRAM_SESSION"])
				
				self.logger.info(f"logged from file, soft login")
				Notify(q_list=self.q_list, error="INSTAGRAM_LOGGED")

				return self.bot

			except :
				self.logger.warning(f"could not log from file, hard login")
				pass

		

		if self.conf['LOGIN_INSTAGRAM'] != "" and self.conf['PASSWORD_INSTAGRAM'] != "":
			sl = 5
			while 1:
				is_auth = False
				try:                    
					is_auth = self.bot.login(self.conf['LOGIN_INSTAGRAM'], self.conf['PASSWORD_INSTAGRAM'])
					self.logger.info(f"instagram logged")
					self.bot.dump_settings(self.conf["INSTAGRAM_SESSION"])
					self.logger.info(f"session dumped")
					break
				
				except Exception as e:
					self.logger.warning(f"instagram login error: {e}")
					# self.logger.warning(f"challange resolver: {self.bot.challenge_code_handler}")
					print(e)
					if str(e) == "EOF when reading a line" or "ChallengeResolve" in str(e):
						# e = Mail_fetcher()
						# code = e.get_code()
						# is_auth = self.bot.login(self.conf['LOGIN_INSTAGRAM'], self.conf['PASSWORD_INSTAGRAM'], verification_code=code)
						
						is_auth = Bypass_email(conf=self.conf).check_process()
						self.bot.load_settings(self.conf["INSTAGRAM_SESSION"])

					if is_auth  == True:
						break
				
				self.logger.info(f"putting instagram to sleep: {sl} seconds")
				time.sleep(sl)
				sl = sl*2

			Notify(q_list=self.q_list, error="INSTAGRAM_LOGGED")
		else:
			Notify(q_list=self.q_list, error="INSTAGRAM_LOGIN_SKIPPED")

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






if __name__  == "__main__":
	path = ""
	insta = Instagram_api()
	insta.login()
	insta.upload_post(img_path=path, caption="hello world 2")


