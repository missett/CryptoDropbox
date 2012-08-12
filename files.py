import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog import events
import network
import encrypt
import string
import xml.etree.ElementTree
from xml.etree.ElementTree import tostring
import settings

class EventHandler( events.FileSystemEventHandler ):
	"""Decides what to do when each event happens on the file system. Supports the usual
	   CRUD operations. Each operation will return a file descriptor that can be passed 
	   to the encryption module. Subclasses the FileSystemEventHandler class from the
	   watchdog module so it can properly handle events."""
	
	def __init__( self , networkHandler , encryptionHandler , settingsManager ):
		self.rootPath = settingsManager.get_folder_path()
		self.networkHandler = networkHandler
		self.encryptHandler = encryptionHandler

	def on_moved( self , event ):
		self.networkHandler.move_file( self.get_dropbox_path( event.src_path ) , self.get_dropbox_path( event.dest_path ) )
		self.networkHandler.delete_file( self.get_dropbox_path( event.src_path ) )

	def on_created( self , event ):
		if event.is_directory:
			self.networkHandler.create_dir( self.get_dropbox_path( event.src_path ) )
		else:
			self.encryptHandler.encrypt( event.src_path , 'tmp' )
			with open( 'tmp' ) as f:
				self.networkHandler.upload_file( self.get_dropbox_path( event.src_path ) , f )

	def on_deleted( self , event ):
		self.networkHandler.delete_file( self.get_dropbox_path( event.src_path ) )

	def on_modified( self , event ):
		if not event.is_directory:
			self.encryptHandler.encrypt( event.src_path , 'tmp' )
			with open( 'tmp' ) as f:
				self.networkHandler.upload_file( self.get_dropbox_path( event.src_path ) , f )
	
	def get_dropbox_path( self , path ):
		return string.replace( path , self.rootPath , "/" )





if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO , format='%(asctime)s - %(message)s' , datefmt='%Y-%m-%d %H:%M:%S')
    #event_handler = LoggingEventHandler()
    
    settings = settings.SettingsManager()
    networking = network.NetworkHandler()
    encryption = encrypt.PacketManager()

    event_handler = EventHandler( networking , encryption , settings )
    
    observer = Observer()
    observer.schedule(event_handler, path=settings.get_folder_path(), recursive=True)
    observer.start()
    
    try:
    	while True:
    		time.sleep(1)
    		
    except KeyboardInterrupt:
		observer.stop()
		observer.join()
