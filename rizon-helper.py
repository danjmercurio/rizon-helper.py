#!/usr/bin/python
__module_name__ = "RizonHelper"
__module_version__ = "1.0"
__module_description__ = "Authenticate and autojoin channels when connecting to Rizon"

class RizonHelper(object):
	def __init__(self, password, channels = {}):
		try:
			import hexchat
		except ImportError:
			hexchat.prnt("Unable to load hexchat bindings. Exiting.")
			raise SystemExit
		self.password = password
		self.channels = channels

		# Verify we are actually on Rizon
		assert hexchat.get_info("network") == "Rizon"

		# Register an event handler to call a function on connect
		hexchat.hook_server("CONNECT", self.identify)


	def identify(self, password):
		"""
		Issue the command to identify to the NickServ bot. 
		The default auto-identify behavior
		of HexChat sends this incorrectly, 
		which is the reason I am writing this script
		"""
		commandString = "msg NickServ IDENTIFY {0}".format(password) # Leading forward-slash not necessary 
		hexchat.command(commandString)
		hexchat.prnt("Sent command to identify.")

		self.join()

		return hexchat.EAT_NONE # returning this value ensures the event is not consumed and other plugins can still use it

	def join(self):
		'''
		Auto-join a few channels on connect
		'''
		for channel in self.channels.values(): hexchat.command("join {0}".format(channel))			


if (__name__ == "__main__"):
	from os import environ, path
	rizon_password = environ["RIZON_PASSWORD"]

	from json import load as parseJSONfromFile
	if os.path.exists('./channels.json'):
		with open('./channels.json', 'r') as file:
			channels = parseJSONfromFile(file)
	else:
		channels = {}

	if (type(rizon_password) == str \
	    and len(rizon_password) \
	      and rizon_password is not None \
	        and False not in [channel.startswith("#") for channel in channels.values()]):
		r = RizonHelper(rizon_password, channels)
	else:
		raise SystemExit("Env variable $RIZON_PASSWORD is empty or not defined")

