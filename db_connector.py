from sqlite3 import connect
from  base64  import b64encode


class Db_connector(object):

	def db_add_img(self):
		
		txt = b64encode(bytes(self.TEXT, 'utf-8'))

		con = connect(self.db_name)
		curs = con.cursor()
		curs.execute(""" 
			INSERT INTO posts 
			(content, title, approved)
			VALUES 
			(?,?,?)
			""",(txt, self.out_image_name, False))
		con.commit()
		con.close()



# create table posts (
#   id integer PRIMARY key AUTOINCREMENT,
#   added dateTime DEFAULT 'now',
#   content text not NULL,
#   title text NOT NULL,
#   approved bool not NULL,
#   approved_by text NULL,
#   approved_date datetime null

#   )
  
  
 











