from instagrapi import Client

login = ""
password = ""

class Instagram_api():
    def login(self, login, password):
        bot = Client()
        bot.login(login, password)
        return bot

    def upload_photo(self, bot, img_path, caption=""):
        bot.photo_upload(
            img_path, 
            caption=caption
        )

    def upload_album(self, bot, imgs_paths, caption=""):
        bot.album_upload(
            imgs_paths,
            caption = caption
        )