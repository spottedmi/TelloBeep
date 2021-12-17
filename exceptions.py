
class Exception_base(Exception):
	def __init__(self, q_list=None, error=None):
		self.q_list = None
		print("Exception")
		print("token invalid")
		if q_list != None:
			self.q_list = q_list

		if error != None:
			self.error = error

		self.send_exception()
	
	def send_exception(self):
		if self.q_list != None:
			disc = self.q_list.get("2main_thread")
			res = {
				"bot_comment": self.error
			}
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



class Post_ratio(Exception):
	q_list = None
	def __init__(self, q_list=None, error=None):
		print("Exception")
		if q_list != None:
			self.q_list = q_list

		if error != None:
			self.error = error
		
		self.send_exception()

	
	def send_exception(self):
		if self.q_list != None:
			disc = self.q_list.get("2main_thread")
			res = {
				"bot_comment": self.error
			}

			disc.put(self.error)






