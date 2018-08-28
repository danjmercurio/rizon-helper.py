#!/usr/bin/python
__module_name__ = "RizonHelper"
__module_version__ = "1.0"
__module_description__ = "Authenticate and autojoin channels when connecting to Rizon"

class RizonHelper(object):

	def __init__(self, password, channels = {}, nick = None):
		try:
			import hexchat
		except ImportError:
			hexchat.prnt("Unable to load hexchat bindings. Exiting.")
			raise SystemExit
		self.password = password
		self.channels = channels
		self.nick = nick

	def register_event_handlers(self):
		'''
		Register an event handler to call a function
		upon connecting to the server.
		'''

		#assert hexchat.get_info("network") == "Rizon" 	# Verify we are actually on Rizon
		
		hexchat.hook_server("XP_TE_CONNECT", lambda a: hexchat.prnt("Connecting event emitted."))
		hexchat.hook_server("SERVERCONNECTED", self.identify)

	def identify(self):
		"""
		Issue the command to identify to the NickServ bot. 
		The default auto-identify behavior
		of HexChat sends this incorrectly, 
		which is the reason I am writing this script
		"""
		if self.nick: assert self.nick == hexchat.get_info("nick") # Ensure we are authenticating for the right account

		commandString = "msg NickServ IDENTIFY {0}".format(self.password) # Leading forward-slash not necessary 
		hexchat.command(commandString)
		hexchat.prnt("Sent command to identify.")

		return hexchat.EAT_NONE # Returning this value ensures the event is not consumed and other plugins can still use it

	def join(self):
		"""
		Auto-join a few channels on connect
		"""
		for channel in self.channels.values(): hexchat.command("join {0}".format(channel))			


if (__name__ == "__main__"):
	"""
	The NickServ password itself will be stored as an environment variable
	called $RIZON_PASSWORD and defined in ~/.zshrc in my case or ~/.bashrc 
	if one is using the default shell, that is, bash. The IRC nickname is stored
	as an environment value as well.
	"""
	from os import environ; from os.path import exists as path_exists
	rizon_password = environ.get("RIZON_PASSWORD")
	rizon_nick = environ.get("RIZON_NICK")

	"""
	The channels to join after connecting are stored in a flat json file
	including a brief description
	"""
	from json import load as parseJSONfromFile
	if path_exists("./channels.json"):
		with open("./channels.json", "r") as file:
			channels = parseJSONfromFile(file)
	else:
		channels = {"Rizon Support" : "#help"}

	if (type(rizon_password) == str \
	    and len(rizon_password) \
	      and rizon_password is not None \
	        and False not in [channel.startswith("#") for channel in channels.values()]):
		r = RizonHelper(rizon_password, channels, rizon_nick)
		r.register_event_handlers()
		r.join()
	else:
		raise SystemExit("Environment variable $RIZON_PASSWORD is empty, undefined, the wrong type, \
		                 or the channels.json file contains invalid data")

