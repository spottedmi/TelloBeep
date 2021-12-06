from instagrapi import Client
from notifications import Notify

from config import Config


class Instagram_api(Config):
    bot = None
    q_list=None
    def __init__(self, q_list=None):
        super().__init__()
        if q_list != None:
            self.q_list = q_list


    def login(self):
        self.bot = Client()
        self.bot.set_proxy("http://80.211.246.8:8080")
        print("proxy set")
        self.bot.login(self.LOGIN_INSTAGRAM, self.PASSWORD_INSTAGRAM)
        print("bot logged")
        Notify(q_list=self.q_list, error="INSTAGRAM_LOGGED")

        return self.bot

    def upload_post(self, img_path, caption=""):
        self.bot.photo_upload(
            img_path, 
            caption=caption
        )

    def upload_album(self, imgs_paths, caption=""):
        self.bot.album_upload(
            imgs_paths,
            caption = caption
        )


if __name__  == "__main__":
    path = ""
    insta = Instagram_api()
    insta.login()
    insta.upload_post(img_path=path, caption="hello world 2")