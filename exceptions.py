
class Exception_base(Exception):
	def __init__(self, q_list=None, error=None, img=None):
		self.q_list = None

		if q_list != None:
			self.q_list = q_list

		if error != None:
			self.error = error
		
		if img != None:
			self.img = img

		self.send_exception()
	
	def send_exception(self):
		if self.q_list != None:
			disc = self.q_list.get("2main_thread")
			res = {
				"bot_comment": self.error
			}
			if self.img:
				res["filename"] = self.img

			disc.put(res)


class TokenInvalid(Exception_base):
	def __init__(self, q_list=None, error=None):
		super().__init__(q_list=q_list, error="token is invalid")

class TokenReadImpossible(Exception_base):
	def __init__(self, q_list=None, error=None):
		super().__init__(q_list=q_list, error="token read impossible")


class ConnectionTimeout(Exception_base):
	def __init__(self, q_list=None, error=None):
		super().__init__(q_list=q_list, error="tellonym conneciotn timeout")

class CaptchaRequired(Exception_base):
	def __init__(self, q_list=None, error=None):
		super().__init__(q_list=q_list, error="tellonym conneciotn timeout")

class Post_ratio(Exception_base):
	def __init__(self, q_list=None, error=None, img=None):
		super().__init__(q_list=q_list, error="post ratio", img=img)




