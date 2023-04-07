from instagrapi import Client
from TelloBeep.notify import Notify


from TelloBeep.config import conf
from TelloBeep.logs.logger import logger

from TelloBeep.email.email_fetcher import Mail_fetcher
from TelloBeep.email.bypass import Bypass_email

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

		except :
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
						
						is_auth = Bypass_email().check_process()
						self.bot.load_settings(conf["INSTAGRAM_SESSION"])

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


