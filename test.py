import multiprocessing

from run import TelloBeep 


# tellobeep1 = TelloBeep()
# tellobeep1.conf["INSTAGRAM_SESSION"] = "/etc/tellobeep/instagram_session.jsonTEST"
# tellobeep1.run()


def tb1():
	tellobeep1 = TelloBeep(config="/etc/tellobeep/config.jsonTEST")
	# tellobeep1.conf["INSTAGRAM_SESSION"] = "/etc/tellobeep/instagram_session.jsonTEST"
	tellobeep1.run()

def tb2():
	tellobeep1 = TelloBeep(config="/etc/tellobeep/config.jsonPROD")
	# tellobeep1.conf["INSTAGRAM_SESSION"] = "/etc/tellobeep/instagram_session.jsonPROD"
	tellobeep1.run()


# Create two processes
process1 = multiprocessing.Process(target=tb1)
process2 = multiprocessing.Process(target=tb2)

# Start both processes
process1.start()
process2.start()

# Wait for both processes to finish
process1.join()
process2.join()
