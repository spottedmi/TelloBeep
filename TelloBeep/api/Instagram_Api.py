from instagrapi import Client
from TelloBeep.notify import Notify


from TelloBeep.config import conf
from TelloBeep.logs.logger import logger


class Instagram_api():
    bot = None
    q_list=None
    def __init__(self, q_list=None):
        self.logger = logger(name=__name__)
        
        if q_list != None:
            self.q_list = q_list


    def login(self):
        self.bot = Client()
        try:
            self.bot.load_settings(conf["INSTAGRAM_SESSION"])
            self.logger.info(f"logged from file, soft login")
            Notify(q_list=self.q_list, error="INSTAGRAM_LOGGED")

            return self.bot

        except FileNotFoundError:
            self.logger.warning(f"could not log from file, hard login")
            pass

        

        if conf['LOGIN_INSTAGRAM'] != "" and conf['PASSWORD_INSTAGRAM'] != "":
            self.bot.login(conf['LOGIN_INSTAGRAM'], conf['PASSWORD_INSTAGRAM'])
            self.logger.info(f"instagram logged")
            self.bot.dump_settings(conf["INSTAGRAM_SESSION"])
            self.logger.info(f"session dumped")

            print("bot logged")
            Notify(q_list=self.q_list, error="INSTAGRAM_LOGGED")
        else:
            Notify(q_list=self.q_list, error="INSTAGRAM_LOGIN_SKIPPED")
            print("bot login skipped")

        return self.bot

    def upload_post(self, img_path, caption=""):
        self.logger.info(f"post uploaded. {img_path}")

        self.bot.photo_upload(
            img_path, 
            caption=caption
        )

    def upload_album(self, imgs_paths, caption=""):
        self.logger.info(f"instagram album loaded, {imgs_paths}")

        self.bot.album_upload(
            imgs_paths,
            caption = caption
        )


if __name__  == "__main__":
    path = ""
    insta = Instagram_api()
    insta.login()
    insta.upload_post(img_path=path, caption="hello world 2")