


class Notify(object):
	def __init__(self, q_list=None,img=None, error=None):
		self.req = {}
		self.q_list = None
		self.img = None
		if q_list != None:
			self.q_list = q_list
		else:
			self.q_list = None
	


		if img != None:
			self.img = img
		else:
			self.img = None
		self.disc = self.q_list.get("2main_thread")
		self.catalog(error=error)

	def catalog(self, error):
		if error == "POST_RATIO_WARNING":
			self.post_ratio_warining()
		elif error == "POST_RATIO_ALERT":
			self.post_ratio_alert()
		elif error == "CANT_SAVE_IMG":
			self.cant_save()
		elif error == "CANT_SAVE_IMG_BACK":
			self.cant_save_BACK()
		elif error == "FONT_NOT_FOND":
			self.font_not_found()
		elif error == "CAPTCHA_REQUIRED":
			self.tello_captcha()
		elif error == "TELLO_RELOGIN":
			self.tello_relogin()
		elif error == "CENSORSHIP_DICT_NOT_FOUNF":
			self.censorship_dict()
		elif error == "PLEASE_WAIT_FEW_MINUTES":
			self.instagram_wait()
		elif error == "INSTAGRAM_LOGGED":
			self.instagram_logged()
		elif error == "RATE_LIMIT_ERROR":
			self.instagram_rate_limit()
		elif error == "INSTAGRAM_ERROR":
			self.instagram_error()
		else:
			self.all_error(error)
		
			

	def post_ratio_warining(self):
		
		self.req["bot_comment"] = f"""POST RATIO WARNING"""
		
		if self.img: self.req["filename"] = self.img
		self.img = None

		self.disc.put(self.req)

	def post_ratio_alert(self):
		self.req["bot_comment"] = f"""**POST RATIO ALERT**"""
		if self.img: self.req["filename"] = self.img
		self.img = None

		self.disc.put(self.req)

	def cant_save(self):
		self.req["bot_comment"] = f"""**cant save in default location**"""
		self.disc.put(self.req)

	def cant_save_BACK(self):
		self.req["bot_comment"] = f"""**cant save in backup location**"""
		self.disc.put(self.req)

	def font_not_found(self):
		self.req["bot_comment"] = f"""**font font found**"""
		self.disc.put(self.req)

	def tello_relogin(self):
		self.req["bot_comment"] = f"""**Tellonym relogin**"""
		self.disc.put(self.req)
	
	def tello_captcha(self):
		self.req["bot_comment"] = f"""**Tellonym captcha**"""
		self.disc.put(self.req)

	def censorship_dict(self):
		self.req["bot_comment"] = f"""**couldn't find swears list**"""
		self.disc.put(self.req)

	def instagram_wait(self):
		self.req["bot_comment"] = f"""**INSTAGRAM: too many requests**"""
		self.disc.put(self.req)

	def instagram_logged(self):
		self.req["bot_comment"] = f"""**INSTAGRAM: succesfully logged in**"""
		self.disc.put(self.req)

	def instagram_rate_limit(self):
		self.req["bot_comment"] = f"""**INSTAGRAM: rate_limi error**"""
		self.disc.put(self.req)

	def instagram_error(self):
		self.req["bot_comment"] = f"""**INSTAGRAM: just error**"""
		self.disc.put(self.req)

	def all_error(self, error):
		self.req["bot_comment"] = f"""{error}"""
		self.disc.put(self.req)
