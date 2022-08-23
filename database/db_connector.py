from sqlite3 import connect
from  base64  import b64encode
from backend.server import User, Posts, db
from sqlalchemy import exc

from config import conf
from datetime import datetime

class Db_connector():
			

	def db_add_img(self):
		txt = self.TEXT		
		try:
			post = Posts()
			
			post.content = txt
			post.title = conf['out_image_name']
			if conf['AUTORUN'] and not self.censor_flag:
				post.approved = True
				post.approved_by = 0
			else:
				post.approved = None
				post.approved_by = None



			post.approved_date = datetime.now()
			post.users_ip = self.tell_ip
			print(post.users_ip)

			db.session.add(post)
			db.session.commit()

		except exc.IntegrityError as e:
			db.session.rollback()
			self.TEXT = None
			print(e)
			print("___XDDD___")


	def db_set_approved(self, state=True):

		post = Posts.query.filter_by(title=conf['out_image_name']).one()
		if state:
			post.approved_by = 1
		else:
			post.approved_by = None

		
		post.approved = state
		post.approved_date = datetime.now()
		post.content = self.TEXT

		db.session.commit()




	def if_logged(self,user=None, db_name=None, password=""):

		con = connect("db.sqlite")

		curs = con.cursor()
		curs.execute(""" 
			SELECT password from users WHERE username=?;
			""",(user, ))
		try:
			passwd = curs.fetchall()[0][0]
		except:
			return False

		con.close()
		if password == passwd:
			return True
		else:
			return False


# create table posts (
#   id integer PRIMARY key AUTOINCREMENT,
#   added dateTime DEFAULT 'now',
#   content text not NULL,
#   title text NOT NULL,
#   approved bool not NULL,
#   approved_by text NULL,
#   approved_date datetime null

#   )
  
# create table users (
#   id integer PRIMARY key AUTOINCREMENT,
#   added dateTime DEFAULT 'now',
#   username text Not NULL,
#   password text not null,
#   permissions integer DEFAULT 10
#   )
  










