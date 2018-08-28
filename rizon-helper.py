#!/usr/bin/python
__module_name__ = "RizonHelper"
__module_version__ = "1.0"
__module_description__ = "Do stuff when connecting to Rizon"

class RizonHelper(object):
	def __init__(self, password, channels = []):
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
		of hexchat sends this incorrectly, 
		which is the reason I am writing this script
		"""
		commandString = "msg NickServ IDENTIFY {0}".format(password) #leading / not necessary 
		hexchat.command(commandString)
		hexchat.prnt("Sent command to identify.")

		# Now autojoin channels
		self.join()

		return hexchat.EAT_NONE

	def join(self):
		for channel in self.channels: hexchat.command("join {0}".format(channel))			


if (__name__ == "__main__"):
	from os import environ

	rizon_password = environ["RIZON_PASSWORD"]
	channels = {
		"4chan irc": "#4chan",
		"8chan irc": "#8chan",
		"/g/ and /prog/":"#/g/technology",
		"Rizon Support": "#Rizon"
		}

	if (type(rizon_password) == str \
	    and len(rizon_password) \
	      and rizon_password is not None \
	        and False not in [channel.startswith("#") for channel in channels.values()]):
		r = RizonHelper(rizon_password, channels)
	else:
		raise SystemExit("Env variable $RIZON_PASSWORD is empty or not defined")

