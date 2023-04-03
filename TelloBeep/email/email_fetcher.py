from TelloBeep.config import conf
from TelloBeep.logs.logger import logger
import poplib, email, re, time

poplib._MAXLINE=20480


class Mail_fetcher():
	def __init__(self):
		self.logger = logger(name=__name__)

		self.server = 'pop3.poczta.onet.pl'
		
		
		if conf.get("EMAIL_SERVER"):
			self.server = conf["EMAIL_SERVER"]
		else:
			self.server = False
			self.logger.critical("email fetcher has no server defined (EMAIL_SERVER)")

		if "@" in conf["LOGIN_INSTAGRAM"]:
			self.username = conf["LOGIN_INSTAGRAM"]
		elif conf.get("EMAIL_LOGIN"):
			self.username = conf["EMAIL_LOGIN"]
		else:
			self.logger.critical("email fetcher no credentails (Email login)")
		
		if conf.get("EMAIL_PASSWORD"):
			self.password = conf["EMAIL_PASSWORD"]
		else:
			self.password = False
			self.logger.critical("email fetcher no credentails (Email login)")

		self.pop_conn = poplib.POP3_SSL(self.server)


	def login(self):
		try:
			self.pop_conn.user(self.username)
			self.pop_conn.pass_(self.password)
		except Exception as e:
			self.logger.error(f"poplib login error: {e}")
			return False
		return True

	def logout(self):
		self.pop_conn.quit()

	def fetch_mails(self):
		num_emails = len(self.pop_conn.list()[1])
		for i in range(num_emails, 0, -1):
			# Fetch the email at the current index
			resp, data, octets = self.pop_conn.retr(i)
			raw_email = b'\r\n'.join(data).decode('utf-8')
			email_msg = email.message_from_string(raw_email)

			# Check if the email subject and sender match our criteria
			subject = email_msg['Subject']
			sender = email.utils.parseaddr(email_msg['From'])[1]
			# print(f"{subject}    -> {sender}")
			if sender == 'security@mail.instagram.com':

				# Extract the security code from the email body
				body = email_msg.get_payload()
				# print(body)
				# match = re.search(r'<font size=3D"6">: (\d+)', body)
				match = re.search(r'<font size=3D"6">(\d+)(\d+)(\d+)(\d+)(\d+)(\d+)', body)
				# print(match)
				if match:

					security_code = match.group()
					security_code = security_code[security_code.index(">")+1:]
					# security_code = match.group(1)
					s_c = security_code[0] + "****" + security_code[-1]
					self.logger.info(f"found security_code: {security_code}")
					# self.logger.info(f"found security_code: {s_c}")
					# print(f'Found security code: {s_c}')
					return security_code
					break
	def get_code(self):
		delay = 30
		self.logger.info(f"\nsleeping before fetching emails: {delay}s")
		time.sleep(delay)
		self.login()
		code = self.fetch_mails()

		self.logout()

		return code


if __name__ == "__main__":
	mail = Mail_fetcher(logger=logger)
	mail.get_code()