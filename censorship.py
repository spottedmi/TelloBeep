

class Censorship(object):

	# def censure_txt(self):
	# 	if not self.BAD_WORDS:
	# 		self.BAD_WORDS = ""

	# 	profanity.load_censor_words_from_file(self.BAD_WORDS)
	# 	self.TEXT = profanity.censor(self.TEXT) 
	
	swears_list = None

	def __init__(self, bad_words="", text=""):
		if not "BAD_WORDS" in globals():
			self.BAD_WORDS = bad_words
		if not "TEXT" in globals():
			self.TEXT = text

		self.load_file(self.BAD_WORDS)
		
	def load_file(self, link):
		with open(link, "r") as f:
			txt = f.read()
			self.swears_list = txt.rsplit("\n")
			
	def censure_txt(self):
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
				# if swear in elem.lower() and len(swear) > 0:
					s = elem[0]
					e = elem[-1]

					elem_rep = s+(len(swear)-2)*"*" + e
					
					self.TEXT = self.TEXT.replace(elem, elem_rep)
		return self.TEXT



if __name__ == '__main__':
	txt = """TESTING STRING WITH SWEARS	"""
	print(txt)
	Censorship(text=txt, bad_words="swears_list.txt")

