from config import Config

from notifications import Notify

class Censorship(Config):

	# swears_list = None
	q_list=None
	def __init__(self, bad_words="", text="", q_list=None):
		super().__init__()
		Config().__init__(child_class=__class__.__name__)
		
		if q_list != None:
			self.q_list=q_list

		self.load_file(self.BAD_WORDS)
		
	def load_file(self, link) -> None:
		try:
			with open(link, "r") as f:
				txt = f.read()
				self.swears_list = txt.rsplit("\n")
		except:
			Notify(q_list=self.q_list, error="CENSORSHIP_DICT_NOT_FOUND")
			self.logger.error(f"couldn't find censorship dictionary")



			

	def censure_txt(self) -> str:
		words = self.TEXT.replace(",", "")
		words = words.replace(".", "")
		words = words.replace("\n", " ")
		words = words.replace("\t", " ")


		words = words.split(" ")

		for elem in words:
			elem = elem.replace(" ", "")
			elem_low = elem.lower()

			for swear in self.swears_list:
				if swear in elem.lower() and len(swear) > 0:
					s = elem[0]
					e = elem[-1]

					elem_rep = s+(len(swear)-2)*"*" + e
					
					self.TEXT = self.TEXT.replace(swear, elem_rep)
					self.TEXT = self.TEXT.replace(elem, elem_rep)
		return self.TEXT

	def flag_word(self) -> str:
		try:
			text = self.TEXT 
		except:
			text = ""

		self.censure_txt()
		if "*" in self.TEXT:
			self.TEXT = text
			return True
		else:
			self.TEXT = text
			return False




if __name__ == '__main__':
	txt = """ ** Swears here **	"""
	print(txt)
	cen = Censorship(text=txt, bad_words="swears_list.txt")
	cen.TEXT = txt
	print(cen.censure_txt())

