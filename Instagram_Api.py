from instabot import Bot
import glob, os
from config import Config

class Instagram_api(Config):
    ig_bot = None


    def login(self):
        isConfigExists = os.path.isdir("config")
        if(isConfigExists):
            self.clear_cookies()
        self.ig_bot = Bot()
        self.ig_bot.login(username=self.LOGIN_INSTAGRAM, password=self.PASSWORD_INSTAGRAM)
        # self.ig_bot.login(username=login, password=password, is_threaded=True)



    def clear_cookies(self):
        cookie_del = glob.glob("config/*cookie.json")
        os.remove(cookie_del[0])


    def upload_post(self, img_path, caption=""):
        
        self.ig_bot.upload_photo(img_path, caption=caption)


if __name__  == "__main__":
    path = ""
    insta = Instagram_api()
    insta.login()
    insta.upload_post(img_path=path, caption="hello world 2")