import os
import rsa
from rsa import bigfile
import settings
import time

class PacketManager:
	
	def __init__( self ):
		#Check if key files exist, either create them or load them
		try:
			with open("public" , "r") as pub:
				with open("private" , "r") as pri:
					pub,pri.close()
			self.load_existing_keys()
		except:
			self.generate_new_keys()	

		self.settings = settings.SettingsManager()
	
	def generate_new_keys( self ):
		(self.publicKey , self.privateKey) = rsa.newkeys( 512 )

		with open( "public" , 'w' ) as public:
			public.write( self.publicKey.save_pkcs1(format='PEM') )
		public.close()
		
		with open( "private" , 'w' ) as private:
			private.write( self.privateKey.save_pkcs1(format='PEM') )
		private.close()

	def load_existing_keys( self ):
		with open( "public" , 'r' ) as public:
			keydata = public.read()
		public.close()

		self.publicKey = rsa.PublicKey.load_pkcs1( keydata )	

		with open( "private" , 'r' ) as private:
			keydata = private.read()
		private.close()

		self.privateKey = rsa.PrivateKey.load_pkcs1( keydata )

	def encrypt( self , unencryptedFile , encryptedFile ):
		with open( unencryptedFile , 'r' ) as unencrypted:
			with open( encryptedFile , 'w' ) as encrypted:
				bigfile.encrypt_bigfile( unencrypted , encrypted , self.publicKey )

	def decrypt( self , encryptedFile , unencryptedFile ):
		with open( encryptedFile , 'r' ) as encrypted:
			with open( unencryptedFile , 'w' ) as unencrypted:
				bigfile.decrypt_bigfile( encrypted , unencrypted , self.privateKey )

	def encrypt_for_other( self , unencryptedFile , email ):
		with open( 'keys/' + email , 'r' ) as keyfile:
			pKey = rsa.PublicKey.load_pkcs1( keyfile.read() )
		
		destinationPath = self.settings.get_folder_path() + 'Outbox/' + email + time.strftime('-%H-%M-%S') 
		
		with open( destinationPath , 'w' ) as encryptedFile:
			with open( unencryptedFile , 'r' ) as openUnencryptedFile:
				bigfile.encrypt_bigfile( openUnencryptedFile , encryptedFile , pKey )

