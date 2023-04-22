

from TelloBeep.api import Questionmi_api
from TelloBeep.api import Tellonym_api
from TelloBeep.api.handlers.tellonym import Tello_api
from TelloBeep.logs.logger import logger

import sys

class Fetching_api(Tello_api):
	def __init__(self, q_list, conf=None, config_class=None):
		
		if conf:
			self.conf = conf

		self.logger = logger(__name__)

		#questionmi has priority
		if self.conf.get("token_questionmi") != ""  or self.conf.get("questionmi_api_base_url") != "":
			fetch_class = Questionmi_api

		elif self.conf.get("LOGIN_TELLONYM") != "" or self.conf.get("PASSWORD_TELLONYM") != "":
			fetch_class = Tellonym_api
		else:
			self.logger.critical(f"fetching class is not specified, shutting down")
			print("fetching class is not specified, shutting down")
			sys.exit(0)

		self.logger.info(f"fetching class is specified: {fetch_class}")

		super().__init__(q_list, fetch_class=fetch_class, conf=self.conf)