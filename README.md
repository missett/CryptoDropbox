Dependencies -
	
	1) Python RSA by Stuvel
	2) Dropbox Python SDK
	3) Watchdog

	RSA and Watchdog can both be installed with easy_install.
	If you're going to be using this behind a proxy then grab my modified Dropbox SDK, otherwise
	download the latest SDK from the Dropbox Developer website and use the install script. 

Setup -

	You'll need to modify network.py by replacing the hash symbols on line 45 
	with your Dropbox secret and app key. After that you'll need to set up settings.xml
	by adding a folder path for the program to monitor. Don't worry about the public key 
	section as that isn't used by the program anymore. To add more public keys to
	encrypt for, simply drag the key file in PEM format into the 'keys' directory (you 
	may need to create this directory in the same place as the .py files). 

Running-
	
	1) Make sure you've got a directory in the settings.xml file.
	2) Run the python program with 'python daemon.py'. 
		2a) To get the GUI running add a -g command flag after.
