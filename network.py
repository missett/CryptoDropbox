from dropbox import session, rest, client
import pickle
import os

class SessionManager( session.DropboxSession ):
	"""This is the subclass of the Dropbox SDK class that handles all the session
	   and authorisation stuff. Contains a access key and can generate request tokens
	   and urls. Subclassed from the SDK class so we can add new functionality if
	   we need to. """

	def __init__( self , key , secret , accessType ):
		session.DropboxSession.__init__( self , key , secret , accessType )

		self.requestToken = self.get_request_token()
		print "Please visit this URL to authorise your Dropbox account for use with this application:\n" + self.get_auth_url( self.requestToken )
		print "Once you're done there, simply come back here and hit return/enter."
		raw_input()
		self.get_new_access_token(self.requestToken)

	def get_request_token( self ):
		return self.obtain_request_token()

	def get_auth_url( self , requestToken ):
		return self.build_authorize_url( requestToken )

	def get_new_access_token( self , requestToken ):
		return self.obtain_access_token( requestToken )


class NetworkHandler:
	"""This class will handle loading a session object into the client object, both from the
	   Dropbox SDK. It has wrapper functions that call the usual CRUD functions from the 
	   client object as well as a few other metadata functions. Functions that operate on
	   files (uploading, renaming etc) will take a file descriptor of the file on the local
	   system and return True or False on success or fail based on the status code returned 
	   by the Dropbox server."""

	def __init__( self ):
		try:
			self.tokenStore = open( "token" , "r+" )	
		except IOError:
			self.tokenStore = open( "token" , "w" )

		if os.path.getsize( "token" ) == 0:
			self.sessionObject = SessionManager( "##############" , "##############" , "app_folder" )
			pickle.dump( self.sessionObject , self.tokenStore )
		else: 
			self.sessionObject = pickle.load( self.tokenStore )

		self.clientObject = client.DropboxClient(self.sessionObject)

	def upload_file( self , path , file_obj ):
		try:
			self.clientObject.put_file( path , file_obj , overwrite=True )
			return True
		except rest.ErrorResponse:
			return False

	def download_file( self , path , destPath ):
		try:
			data = self.clientObject.get_file( path )
			with open(destPath , 'w') as destFile:
				destFile.write(data)
			
			return True
		except rest.ErrorResponse:
			return False

	def move_file( self , from_path , to_path ):
		try: 
			self.clientObject.file_copy( from_path , to_path )
			return True
		except rest.ErrorResponse:
			return False

	def delete_file( self , path ):
		try:
			self.clientObject.file_delete( path )
			return True
		except rest.ErrorResponse:
			return False

	def create_dir( self , path ):
		try:
			self.clientObject.file_create_folder( path )
			return True
		except rest.ErrorResponse:
			return False
			

if __name__ == '__main__':
	handler = NetworkHandler()

	f = open('public')

	handler.upload_file( '/public' , f )
