from sqlite3 import connect
from  base64  import b64encode
from backend.server import User, Posts, db
from sqlalchemy import exc

class Db_connector(object):

	def db_add_img(self):
		txt = self.TEXT		
		try:
			post = Posts(content=txt, title=self.out_image_name)
			db.session.add(post)
			db.session.commit()
		except exc.IntegrityError as e:
			db.session.rollback()
			self.TEXT = None
			print(e)
			print("___XDDD___")


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
  










