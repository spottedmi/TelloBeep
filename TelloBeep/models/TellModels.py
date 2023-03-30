from TelloBeep.censorship import Censorship
from TelloBeep.config import conf

import time
from datetime import datetime, time, timezone
import pytz

from TelloBeep.logs.logger import logger


class Tells_Utills():

	def __init__(self, tellJSON):
		self.logger = logger(name=__name__)

		# self.title = title
		self.send = False
		self.metadata = self

		self.id = tellJSON["id"]
		
		self.tell = None
		# self.text = self.tell

		self.users_ip = tellJSON.get("users_ip") if tellJSON.get("users_ip") else "0.0.0.0" 

		# self.flag = False

		
		

		self.filename = None

	def time_to_tz_naive(self, t, tz_in, tz_out, index=None):
		if index:
			out = tz_in.localize(datetime.combine(datetime.today(), t)).astimezone(tz_out).time() 
			out = out.replace(hour=out.hour+index)
			return out

		return tz_in.localize(datetime.combine(datetime.today(), t)).astimezone(tz_out).time()

	def find_timezone_name(self, minutes_offset_from_utc):
		for tz in pytz.all_timezones:
				minutes = pytz.timezone(tz).utcoffset(datetime.now()).total_seconds()/60

				if minutes == minutes_offset_from_utc:                
					return tz


	def get_date(self, tellJSON):
	
		try:

			tellJSON, offset = tellJSON.split(".")
			offset = int(offset[:-1])
			offset = int(offset/60)

			offset = self.find_timezone_name(offset)

			d = datetime.strptime(tellJSON, "%Y-%m-%dT%H:%M:%S")
			t = d.time()

			LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo

			
			# print(f"line6.2 {pytz.timezone(f'{offset}')}")
			# print(f"line6.3 {pytz.timezone(f'{LOCAL_TIMEZONE}')}")
			self.logger.critical(LOCAL_TIMEZONE)
			self.logger.critical(LOCAL_TIMEZONE)
			if str(LOCAL_TIMEZONE) == "CEST" or str(LOCAL_TIMEZONE) == "Central European Daylight Time":
				t = self.time_to_tz_naive(t, pytz.timezone(f"{offset}"), pytz.timezone(f"CET"), index=0)
			else:
				t = self.time_to_tz_naive(t, pytz.timezone(f"{offset}"), pytz.timezone(f"{LOCAL_TIMEZONE}"))


			d = d.replace(hour=t.hour)

			return d.strftime(format="%Y-%m-%dT%H:%M:%S")

		except Exception as e:
			print(f"error {e}")
			pass

		try:	
			d = datetime.strptime(tellJSON, "%Y-%m-%dT%H:%M:%S.%f")

			d = d.replace(hour=time.localtime().tm_hour)

			return d.strftime(format="%Y-%m-%dT%H:%M:%S.000Z")
		except Exception as e:
			print(e)

			pass


	def get_title(self, dtime):
			tm , date = dtime.rsplit("T")
			y, M, d = tm.rsplit("-")
			if len(M) == 1: M = f"0{M}"
			date = date.rsplit(".")[0]
			
			h,m,s = date.rsplit(":")

			if len(h) == 1: h = f"0{h}"
			if len(m) == 1: m = f"0{m}"
			if len(s) == 1: s = f"0{s}"
	
			if h == 24:
				self.logger.info(f"24 hour detected")
				h = "00"

			title = f"{y}{M}{d}{h}{m}{s}_{self.id}"
			print(title)
			return title

	def __str__(self):
		return self.tell


class Questionmi_tell(Tells_Utills):
	def __init__(self, tellJSON):
		super().__init__(tellJSON)

		self.tell = tellJSON["text"]
		# self.created_at = tellJSON["created_at"]
		# self.users_ip = tellJSON["users_ip"]
		# conf['user']s_fingerprint = tellJSON["users_fp"]
		
		self.created_at = self.get_date(tellJSON["created_at"])
		self.title = self.get_title(self.created_at)

		

		self.cen = Censorship()
		self.cen.TEXT = self.tell
		self.flag  = self.cen.flag_word()


		


class Tellonym_tell(Tells_Utills):
	def __init__(self, tellJSON):
		super().__init__(tellJSON)

		self.tell = tellJSON["tell"]
		# self.users_ip = "0.0.0.0"

		# self.flag = False

		self.created_at = self.get_date(tellJSON["createdAt"])
		

		self.title = self.get_title(self.created_at)

		
		self.cen = Censorship()
		self.cen.TEXT = self.tell
		self.flag  = self.cen.flag_word()





class Questionmi_user():
	def __init__(self, tokenJSON):		
		user_id = tokenJSON["userId"]
		self.token = tokenJSON["accessToken"]


class Tellonym_user():
	def __init__(self, tokenJSON):
		user_id = tokenJSON["userId"]
		self.token = tokenJSON["accessToken"]

		