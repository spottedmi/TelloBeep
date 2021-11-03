import cloudscraper

class TellonymTell():
	def __init__(self, tellJSON):
		# for elem in tellJSON:
		# 	x = eval(f"tellJSON['{elem}']")
		# 	print(f"{elem} :  {x}")

		self.question = tellJSON["tell"]
		self.answer = tellJSON["answer"]
		self.createdAt = tellJSON["createdAt"]
		self.likeCount = tellJSON["likesCount"]

class TellonymUser():
	def __init__(self, profileJson):
		self.profielPropeties = profileJson

		self.cSession = cloudscraper.create_scraper()
		self.display_name = profileJson["displayName"]
		self.username = profileJson["username"]
		self.bio = profileJson["aboutMe"]
		self.avatar_url = profileJson["avatarFileName"]
		self.user_id = profileJson["id"]
		self.followersCount = profileJson["followerCount"]
		self.anonymousFollowerCount = profileJson["anonymousFollowerCount"]
		self.isFollowingcount = profileJson["followingCount"]
		self.active = profileJson["isActive"]
		self.tellsCount = profileJson["tellCount"]
		self.tells = []
		self.followers = []
		self.followings = []

	def FetchTells(self):
		self.tells = []
		tellsUrl = "https://api.tellonym.me/answers/{}?&userId={}&limit=25&pos={}"
		posX = 0
		while True:
			tellReq = self.cSession.get(tellsUrl.format(str(self.user_id), str(self.user_id), str(posX)))
			respJs = tellReq.json()
			if len(respJs["answers"]) == 0:
				break
	
			for xT in respJs["answers"]:
				if xT["type"] == "AD":
					continue
				else:
					self.tells.append(TellonymTell(xT))
	
			self.tells.reverse()
			posX += 25

class TellonymApi():
	def __init__(self):
		self.api_url = "https://api.tellonym.me"
		self.cSession = cloudscraper.create_scraper()

	def GetUser(self, username):
		request = self.cSession.get("{}/profiles/name/{}".format(self.api_url, username))
		if request.status_code == 200:
			return TellonymUser(request.json())
		else:
			return TellonymUser(None)


class Get_questions(TellonymApi):
	def __init__(self):
		super().__init__()
		user = self.GetUser("spotted_kasprzak_auto")
		user.FetchTells()

		for tell in user.tells:
			print(tell.question)

