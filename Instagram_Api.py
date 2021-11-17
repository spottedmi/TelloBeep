from instabot import Bot
import glob, os

login = ""
password = ""

class Instagram_api():
    def Clear_cookies(self):
        cookie_del = glob.glob("config/*cookie.json")
        os.remove(cookie_del[0])

    def Upload_post(self, img_path):
        isConfigExists = os.path.isdir("config")
        if(isConfigExists):
            self.Clear_cookies
        
        ig_bot = Bot()
        ig_bot.login(username=login, password=password)
        ig_bot.upload_photo(img_path, caption="")
