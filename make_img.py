#!/usr/bin/python3
#by RandomGuy90 A.D.2021

from PIL import Image, ImageDraw, ImageFont
import random, time

from queue import Queue
import _thread

from censorship import Censorship
from db_connector import Db_connector

class Make_img(Censorship, Db_connector):
	def __init__(self, q_list=None):
		super().__init__()
		

		if q_list:
			self.q_list = q_list
			self.load_from_threads()

	def gen(self) -> None:
		"generate image"
		self.prepare_text()
		self.get_fonts()
		self.get_size_txt()
		self.set_margins()

		# img = Image.new('RGB', (self.width, self.height), self.hex_to_rgb(self.colorBackground))
		self.img_object = Image.new('RGB', (self.width, self.height), self.hex_to_rgb(self.colorBackground))
		d = ImageDraw.Draw(self.img_object)
		
		#text 
		coords =(self.margin["left"] ,self.margin["top"])
		
		d.text(coords, self.TEXT, fill=self.hex_to_rgb(self.colorText), font=self.font)
		d.rectangle((0, 0, self.width-self.outline_thickness, self.height-self.outline_thickness),width= self.outline_thickness, fill=None, outline=self.hex_to_rgb(self.colorOutline))

		#header
		self.create_header()

		#footer
		self.create_footer()

		img = Image.open(self.image_path, "r")
		img = img.resize(self.image_size, Image.ANTIALIAS)
		img = img.convert("RGBA")

		coords = (int(self.insta_res[1]*0.82), int(self.insta_res[0]*0.73))

		self.img_object.paste(img, coords, img)

		#resizing and prepare to save
		img = img.convert("RGB")
		self.save_img()
		self.save_tumbnail()
		
		self.db_add_img()

		insta = self.q_list.get("2insta")
		if self.AUTORUN:
			req = {
				"text": f"{self.out_image_name}.{self.extension}",
				"title": self.TEXT,
				"send": True
			}
			insta.put(req)
	
		

		# if self.AUTORUN:
		# 	self.db_set_approved()



	def save_img(self):
		self.img_object = self.img_object.resize(self.insta_res, Image.ANTIALIAS)
		self.filename = f"{self.out_image_path}/{self.out_image_name}.{self.extension}"
		self.img_object.save(self.filename)

	def save_tumbnail(self):
		self.img_object = self.img_object.resize(self.thumb_res, Image.ANTIALIAS)
		self.img_object.save(f"{self.thumb_path}/{self.out_image_name}_thumbnail.{self.extension}")
		
	def get_size_txt(self)-> None:
		"get size of text object"

		testImg = Image.new('RGB', (1, 1))
		testDraw = ImageDraw.Draw(testImg)
		width, height = testDraw.textsize(self.TEXT, self.font)
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
		ftr.text(footer_coords, self.TEXT_footer, fill=self.hex_to_rgb(self.colorText), font=self.font_footer)

	def create_header(self) -> None:
		"creating footer with posting date"
		self.create_data()
		header = ImageDraw.Draw(self.img_object)
		header_coords = (self.margin["left"], self.insta_res[1]*0.04)
		header.text(header_coords, self.DATE, fill=self.hex_to_rgb(self.colorText), font=self.font_footer)

		
	def create_data(self) -> None:
		"create data if not specified for header"
		if self.DATE == None:
			date = time.localtime()
			yr = date.tm_year
			month  = str(date.tm_mon) if len(str(date.tm_mon)) == 2 else f"0{date.tm_mon}"
			day  = str(date.tm_mday) if len(str(date.tm_mday)) == 2 else f"0{date.tm_mday}"
			hour  = str(date.tm_hour) if len(str(date.tm_hour)) == 2 else f"0{date.tm_hour}"
			minutes  = str(date.tm_min) if len(str(date.tm_min)) == 2 else f"0{date.tm_min}"
			mil = int(round(time.time() * 1000))
			self.DATE = f"{hour}:{minutes} {day}/{month}/{yr}"



	def prepare_text(self) -> str:
		"cut text and prepare to show"

		txt = self.TEXT.rsplit(" ")
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

		self.TEXT = str(res_txt)

		self.censure_txt()

	def load_from_threads(self):

		while 1:
			gen = self.q_list.get("2gen")
			insta = self.q_list.get("2insta")
			# q2 = self.q_list.get("2flask")
			# q2 = self.q_list.get("2tello")
			res = gen.get() 
			
			#res =  q2.get()

			data = res["text"]
			self.out_image_name = res["title"]
			t = res["title"]
			#2021 10 22 11 03 53
			self.DATE = f"{t[8]}{t[9]}:{t[10]}{t[11]} {t[6]}{t[7]}/{t[4]}{t[5]}/{t[0:4]}"

			self.TEXT_tmp = data
			if data:
				self.TEXT = data
				self.gen()

			if res.get("send"):
				res = {
				"title": self.out_image_name
				}

				insta.put(res)
				 
			else:
				pass
			


			time.sleep(0.01)
			



if __name__ == '__main__':

	asd = Make_img()
	asd.gen()
