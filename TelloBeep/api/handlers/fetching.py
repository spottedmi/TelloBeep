from TelloBeep.config import conf

from TelloBeep.api import Questionmi_api
from TelloBeep.api import Tellonym_api
from TelloBeep.api.handlers.tellonym import Tello_api


class Fetching_api(Tello_api):
	def __init__(self, q_list):

		#questionmi has priority
		if conf.get("token_questionmi") != ""  or conf.get("questionmi_api_base_url") != "":
			fetch_class = Questionmi_api

		elif conf.get("LOGIN_TELLONYM") != "" or conf.get("PASSWORD_TELLONYM") != "":
			fetch_class = Tellonym_api
		else:
			conf["logger"].critical(f"fetching class is not specified, shutting down")
			print("fetching class is not specified, shutting down")
			sys.exit(0)

		conf["logger"].info(f"fetching class is specified: {fetch_class}")

		super().__init__(q_list, fetch_class=fetch_class)