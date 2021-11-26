from instagrapi import Client

from config import Config


class Instagram_api(Config):
    bot = None


    def login(self):
        bot = Client()
        bot.login(login=LOGIN_INSTAGRAM, password=PASSWORD_INSTAGRAM)
        return bot

    def upload_photo(self, img_path, caption=""):
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