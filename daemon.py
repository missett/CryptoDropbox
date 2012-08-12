import settings
import network
import encrypt
import files
import menu

import time
import sys

from watchdog.observers import Observer

if __name__ == '__main__':
	try:	
		if sys.argv[1] == '-g':
			print 'Using GUI'
			menu.UISetup()
	except: 
		print 'Using Command Line'

	settings = settings.SettingsManager()
	networking = network.NetworkHandler()
	encryption = encrypt.PacketManager()

	handler = files.EventHandler( networking , encryption , settings )

	observer = Observer()
	observer.schedule( handler , path=settings.get_folder_path() , recursive=True )
	observer.start()

	while True:
		time.sleep(1)
