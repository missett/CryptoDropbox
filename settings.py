import xml.etree.ElementTree
from xml.etree.ElementTree import tostring
import os

class SettingsManager( xml.etree.ElementTree.ElementTree ):
	""" This class will load the settings.xml file and parse it to correctly return the user
		controlled settings. Does not parse the list of public and private keys until requested
		so that memory usage is conserved."""

	def __init__( self ):
		self.parse("settings.xml")

	def get_help( self ):
		return self.getroot().find("settings").find("help").text

	def get_folder_path( self ):
		return self.getroot().find("settings").find("folder_path").text

	def set_folder_path( self , newPath ):
		self.getroot().find("settings").find("folder_path").text = newPath
		with open("settings.xml" , "w") as settings:
			settings.write(tostring(self.getroot()))

	def get_refresh_rate( self ):
		return self.getroot().find("settings").find("refresh_rate").text

	def set_refresh_rate( self , newRate):
		self.getroot().find("settings").find("refresh_rate").text = newRate
		with open("settings.xml" , "w") as settings:
			settings.write(tostring(self.getroot()))

	def get_key_list( self ):
		result = os.listdir('keys/')
		result.pop(0) #Get rid of DS_Store in keys directory
		return result


	def set_new_key( self , email , public , private ):
		#New user element
		newElement = xml.etree.ElementTree.Element( "user" , attrib={"email":email} ) 
		#New public key element
		publicElement = xml.etree.ElementTree.Element( "public" )
		publicElement.text = public
		#New private key element
		privateElement = xml.etree.ElementTree.Element( "private" )
		privateElement.text = private
		#Append both to the new key element
		newElement.append( publicElement )
		newElement.append( privateElement )
		#Attach new user to the tree
		self.getroot().find("keys").append( newElement )

		with open("settings.xml" , "w") as settings:
			settings.write( tostring( self.getroot() ) )

