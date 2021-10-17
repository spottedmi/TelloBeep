#!/usr/bin/python3
#by RandomGuy90 A.D.2021

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Make_img(object):
	def __init__(self):

		#img config
		self.text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum  """
		self.text_footer = """FOOTER_INFO"""

		self.imageName = "image.png"
		self.margin = {
			"top":20,
			"right":20,
			"bottom":20,
			"left":20
		}
		self.height = 0
		self.width = 0
		
		#fonts
		self.fontname = "/usr/share/fonts/TTF/Arial.TTF"

		#footer config
		self.font_footer_name = "./Anton.ttf"
		self.font_footer_size = 55
		self.font_footer = None
		self.footer_height = 100


		self.fontsize = 31
		self.font = None

		#colors
		self.colorBackground= "#1C1936"
		self.colorOutline = "#ffffff"
		self.colorText  = "#ffffff"

		#text config
		self.word_break = 10

		self.header = "KASPRZAK SPOTTED"

		#outline
		self.outline_thickness = 4

		#instagram resolution
		self.insta_res = (1080, 1080)
		# self.insta_res = (1350, 1080)
		# self.insta_res = (1608, 1080)


	def gen(self) -> None:
		"generate image"

		self.prepare_text()
		self.get_fonts()
		self.get_size_txt()
		self.set_margins()

		# img = Image.new('RGB', (self.width, self.height), self.hex_to_rgb(self.colorBackground))
		img = Image.new('RGB', (self.width, self.height), self.hex_to_rgb(self.colorBackground))
		d = ImageDraw.Draw(img)
		
		coords =(self.margin["left"] ,self.margin["top"])
		
		d.text(coords, self.text, fill=self.hex_to_rgb(self.colorText), font=self.font)
		d.rectangle((0, 0, self.width-self.outline_thickness, self.height-self.outline_thickness),width= self.outline_thickness, fill=None, outline=self.hex_to_rgb(self.colorOutline))

		ftr = ImageDraw.Draw(img)
		footer_coords = (self.margin["left"], self.insta_res[1]*0.75)
		print(footer_coords)
		ftr.text(footer_coords, self.text_footer, fill=self.hex_to_rgb(self.colorText), font=self.font_footer)

		# img.save("image.png", quality=20, optimize=True)
		img = img.resize(self.insta_res, Image.ANTIALIAS)
		img.save("image.png")

	def get_size_txt(self)-> None:
		"get size of text object"

		testImg = Image.new('RGB', (1, 1))
		testDraw = ImageDraw.Draw(testImg)
		width, height = testDraw.textsize(self.text, self.font)
		self.heightTXT = height
		self.widthTXT = width
		
		self.width = height if height > width else width
		self.height = width if width > height else height

	def hex_to_rgb(self, value) -> tuple:
		"convert hex value to rgb"

		value = value.lstrip('#')
		lv = len(value)
		return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

	def get_fonts(self) -> None:
		"import fonts"
		
		self.font = ImageFont.truetype(self.fontname, self.fontsize)
		self.font_footer = ImageFont.truetype(self.font_footer_name, self.font_footer_size)

	def set_margins(self) -> None:
		"margins"

		self.margin["top"] = (self.height - self.heightTXT) / 2 - self.footer_height
		self.margin["left"] = (self.width * 5) / 100
		
		self.width = int(self.width+(self.margin["left"]*2))
	
	def prepare_text(self) -> str:
		"cut text and prepare to show"

		txt = self.text.rsplit(" ")
		res_txt = ""
		words = self.word_break
		i = 0 
		for elem in txt:
			i+=1
			# res_txt.append(elem)
			res_txt = res_txt +" "+ elem
			#print(res_txt)
			if not i%words:
				res_txt = res_txt + "\n"

		self.text = str(res_txt)








if __name__ == '__main__':

	asd = Make_img()
	asd.gen()