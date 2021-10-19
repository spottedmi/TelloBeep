from better_profanity import profanity

class Censorship(object):

	def censure_txt(self):
		if not self.BAD_WORDS:
			self.BAD_WORDS = ""

		profanity.load_censor_words_from_file(self.BAD_WORDS)
		self.TEXT = profanity.censor(self.TEXT) 





if __name__ == '__main__':
	Censorship()

