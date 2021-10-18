#!/usr/bin/python3
#by RandomGuy90 A.D.2021

from PIL import Image, ImageDraw, ImageFont
import random

class Make_img(object):
	def __init__(self):

		#img config
		self.text_tmp = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum """
		self.text_tmp = self.text_tmp.split(" ")
		self.text = ""
		for elem in range(random.randrange(0, 100)):
			self.text +=f" {self.text_tmp[elem]}"
		print(self.text)
		print(F"LENGHT {len(self.text)}")
		# if len(self.text) <300:
		# 	self.text += (400-len(self.text))*" "
		print(self.text)
		print(F"LENGHT {len(self.text)}")


		self.text_footer = """#FOOTER_TEXT_FOOTER_TEXT"""

		self.imageName = "image.png"
		self.margin = {
			"top":20,
			"right":20,
			"bottom":20,
			"left":20
		}
		self.height = 0
		self.width = 0
		self.img_object = None

		#fonts
		self.fontname = "/usr/share/fonts/TTF/Arial.TTF"
		self.fontsize = 31
		self.font = None

		#footer config
		self.font_footer_name = "./Anton.ttf"
		self.font_footer_size = 65
		self.font_footer = None
		self.footer_height = 100
		#footer image config
		self.image_path = "./LogoTemplate.png"
		self.image_size = (250, 250)

		#colors
		self.colorBackground= "#1C1936"
		self.colorOutline = "#ffffff"
		self.colorText  = "#ffffff"

		#text config
		self.word_break = 10


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
		self.img_object = Image.new('RGB', (self.width, self.height), self.hex_to_rgb(self.colorBackground))
		d = ImageDraw.Draw(self.img_object)
		
		coords =(self.margin["left"] ,self.margin["top"])
		
		d.text(coords, self.text, fill=self.hex_to_rgb(self.colorText), font=self.font)
		d.rectangle((0, 0, self.width-self.outline_thickness, self.height-self.outline_thickness),width= self.outline_thickness, fill=None, outline=self.hex_to_rgb(self.colorOutline))

		self.create_footer()

		img = Image.open(self.image_path, "r")
		img = img.resize(self.image_size, Image.ANTIALIAS)
		img = img.convert("RGBA")

		coords = (int(self.insta_res[1]*0.82), int(self.insta_res[0]*0.73))

		self.img_object.paste(img, coords, img)

		self.img_object = self.img_object.resize(self.insta_res, Image.ANTIALIAS)
		self.img_object.save("image.png")



	def get_size_txt(self)-> None:
		"get size of text object"

		testImg = Image.new('RGB', (1, 1))
		testDraw = ImageDraw.Draw(testImg)
		width, height = testDraw.textsize(self.text, self.font)
		self.heightTXT = height
		self.widthTXT = width
		
		# self.width = height if height > width else width
		# self.height = width if width > height else height

		self.width = self.insta_res[0]
		self.height = self.insta_res[1]

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
	
	def create_footer(self) -> None:
		"creating image's footer"

		ftr = ImageDraw.Draw(self.img_object)
		footer_coords = (self.margin["left"], self.insta_res[1]*0.85)
		# print(footer_coords)
		ftr.text(footer_coords, self.text_footer, fill=self.hex_to_rgb(self.colorText), font=self.font_footer)

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