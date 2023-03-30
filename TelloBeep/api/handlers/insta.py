from queue import Queue
import time, random, json, os, sys

from TelloBeep.api import Instagram_api

from instagrapi.exceptions import PleaseWaitFewMinutes, RateLimitError, PhotoNotUpload
from TelloBeep.config import conf
from TelloBeep.notify import Notify
from TelloBeep.logs.logger import logger


#_____________________________________________________________
#
#               INSTAGRAM API
#_____________________________________________________________

class Insta_api():
	def __init__(self, q_list):
		self.logger = logger(name=__name__)
		
		print("instaapi")

		"this is only a makeshift"
		"fetching api function's going to replace this"

		self.q_list = q_list
		self.insta = Instagram_api(q_list=self.q_list)

		delay = 10
		while True:
			try:
				self.insta.login()
				break
			except PleaseWaitFewMinutes :
				Notify(q_list=self.q_list, error="PLEASE_WAIT_FEW_MINUTES")
				self.logger.warning(f"PLEASE_WAIT_FEW_MINUTES instagram login delay: {delay}")

				time.sleep(delay)
			except RateLimitError:
				Notify(q_list=self.q_list, error="RATE_LIMIT_ERROR")
				self.logger.warning(f"RATE_LIMIT_ERROR instagram login delay: {delay}")

				# time.sleep(delay)

			except Exception as e:
				print(e)
				Notify(q_list=self.q_list, error="INSTAGRAM_ERROR")
			
			time.sleep(delay)
			delay += 2 * delay

		self.recv_mgs()

	def recv_mgs(self) -> None:
		q = self.q_list.get("2insta")

		while 1 :
			content = q.get()
			# print(f"INSTAGRAM {content['title']}")

			path = f"{conf['out_image_path']}/{content['filename']}"

			if conf['CAPTION'] != "":
				pass
				self.send_post(path, caption=conf["CAPTION"])
				# self.insta.upload_post(path, caption=conf['CAPTION'])
			else:
				pass
				self.send_post(path, caption=conf["CAPTION"])
				# self.insta.upload_post(path)
			# print("instagram sent")

			time.sleep(0.1)

	def send_post(self, path, caption=None):
		sleep = 5
		while True:
			try:
				if caption:
					self.insta.upload_post(path, caption=caption)
				else:
					self.insta.upload_post(path)

				break

			except PhotoNotUpload as e:
				self.logger.warning(f"cannot upload photo: PhotoNotUpload")
				self.logger.warning(f"go to sleep for: {sleep}")
				# self.logger.info(f"cannot upload photo: {e}")
				Notify(q_list=self.q_list, error="PhotoNotUpload error")
				time.sleep(sleep)
				sleep = sleep * 2

				self.insta.login()



