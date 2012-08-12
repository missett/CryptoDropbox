import Tkinter
import ttk
import os
import settings
import encrypt

class myGUI(Tkinter.Frame):
	def __init__( self , parent ):
		Tkinter.Frame.__init__( self , parent )
		self.parent = parent
		self.parent.title("Crypto Dropbox")

		#Top Frame
		topFrame = Tkinter.Frame( self , width=400 , height=250 )
		
		self.notebook = ttk.Notebook( topFrame , width=400 , height=220 ) 
		self.notebook.pack( fill=Tkinter.BOTH )

		#Create the frame objects for the tabs so we can reference them later
		self.settingsFrame = Settings(self.notebook)

		#Add the frame to the notebook as tabs
		self.notebook.add( self.settingsFrame , text='Settings' )
		self.notebook.add( Decrypt(self.notebook) , text='Decrypt' )
		self.notebook.add( Sharing(self.notebook) , text='Sharing' )
		self.notebook.add( Help(self.notebook) , text='Help' )

		topFrame.pack(side=Tkinter.TOP)
		
		#Bottom Frame
		bottomFrame = Tkinter.Frame( self , width=400 , height=50 )
		
		applyButton = Tkinter.Button( bottomFrame , text='Apply' , pady=25 , command=self.apply )
		applyButton.pack()
		
		bottomFrame.pack()

		self.pack()

	def apply( self ):
		settingsManager = settings.SettingsManager()
		settingsManager.set_folder_path( self.settingsFrame.e.get() )

class Settings(Tkinter.Frame):
	def __init__( self , parent ):
		Tkinter.Frame.__init__( self , parent )

		#Create the manager so we can get/set things
		settingsManager = settings.SettingsManager()

		self.l = Tkinter.Label( self , text='Folder: ' )
		self.e = Tkinter.Entry( self )
		
		#Insert the current folder path
		self.e.insert( 0 , settingsManager.get_folder_path() )
		
		self.l.pack(side=Tkinter.LEFT , padx=10 , expand=1)
		self.e.pack(side=Tkinter.RIGHT , padx=10 , expand=1)

class Decrypt(Tkinter.Frame):
	def __init__( self , parent ):
		Tkinter.Frame.__init__( self , parent )

		self.settingsManager = settings.SettingsManager()
		self.packetManager = encrypt.PacketManager()

		self.tree = ttk.Treeview(self)

		self.tree.pack(expand=1 , side=Tkinter.LEFT , fill=Tkinter.BOTH)
		self.constructTree(self.settingsManager.get_folder_path() + 'Inbox' , '')

		scroller = Tkinter.Scrollbar(self)
		scroller.pack(side=Tkinter.RIGHT , fill=Tkinter.Y)
		
		self.tree.config(yscrollcommand=scroller.set)
		scroller.config(command=self.tree.yview)

		self.tree.tag_bind('clickable' , '<<TreeviewSelect>>' , self.clicked)

	def clicked( self , *args ):
		c = self.tree.focus()
		encrypted_file = os.path.join( self.settingsManager.get_folder_path() , 'Inbox' , self.tree.item(c)['values'][0] )
		dest_path = os.path.join( self.settingsManager.get_folder_path() , encrypted_file.split('/')[-1] )
		self.packetManager.decrypt( encrypted_file , dest_path )
		print 'Dest Path: ' + dest_path
		print 'Source File: ' + encrypted_file

	def constructTree( self , path , node ):
		#Populate a list of people we can encrypt for

		for i in os.listdir(path):
			if i != 'Outbox': #Make sure to exclude the outbox folder
				n = self.tree.insert(node , 'end' , text=i , tags='clickable' , values=i) 
				if os.path.isdir( os.path.join( path , i ) ):
					self.constructTree( os.path.join( path , i ) , n )
				else:
					pass
					#Need to put the key list in for every element
					#Also add a value representing the full file path of the file
					#for k in keyList:
						#self.tree.insert(n , 'end' , text=k , tags='clickable' , values=( os.path.join(path , i) ))

class Sharing(Tkinter.Frame):
	def __init__( self , parent ):
		#Add in a hook to pull from the XML file
		self.settingsManager = settings.SettingsManager()
		self.encryptManager = encrypt.PacketManager()
		
		#Build basic layout
		Tkinter.Frame.__init__( self , parent )
		self.tree = ttk.Treeview(self)

		self.tree.pack(expand=1 , side=Tkinter.LEFT , fill=Tkinter.BOTH)
		self.constructTree(self.settingsManager.get_folder_path() , '')

		scroller = Tkinter.Scrollbar(self)
		scroller.pack(side=Tkinter.RIGHT , fill=Tkinter.Y)
		
		self.tree.config(yscrollcommand=scroller.set)
		scroller.config(command=self.tree.yview)

		self.tree.tag_bind('clickable' , '<<TreeviewSelect>>' , self.clicked)

	#Use some recursion magic to build the file system tree
	def constructTree( self , path , node ):
		#Populate a list of people we can encrypt for
		keyList = self.settingsManager.get_key_list()

		for i in os.listdir(path):
			if i != 'Outbox' and i != 'Inbox': #Make sure to exclude the outbox and inbox folder
				n = self.tree.insert(node , 'end' , text=i ) 
				if os.path.isdir( os.path.join( path , i ) ):
					self.constructTree( os.path.join( path , i ) , n )
				else:
					#Need to put the key list in for every element
					#Also add a value representing the full file path of the file
					for k in keyList:
						self.tree.insert(n , 'end' , text=k , tags='clickable' , values=( os.path.join(path , i) ))

	def clicked( self , *args ):
		c = self.tree.focus()
		#Email
		print self.tree.item(c)['text']
		#File path
		print self.tree.item(c)['values'][0]
		self.encryptManager.encrypt_for_other( self.tree.item(c)['values'][0] , self.tree.item(c)['text'] )


class Help(Tkinter.Frame):
	def __init__( self , parent ):
		Tkinter.Frame.__init__( self , parent )

		#Create scroll bar
		scroller = Tkinter.Scrollbar( self )
		scroller.pack(side=Tkinter.RIGHT , fill=Tkinter.Y)

		t = Tkinter.Text( self , padx=5 , pady=5 , wrap=Tkinter.WORD )

		#Hook up scrollbar
		t.config(yscrollcommand=scroller.set)
		scroller.config(command=t.yview)
		
		#Insert the text
		settingsManager = settings.SettingsManager()
		t.insert( Tkinter.END , settingsManager.get_help() )
		
		#Disable it and pack it in
		t.configure(state='disabled')
		t.pack(expand=1)

class UISetup():
	def __init__( self ):
		root = Tkinter.Tk()
		main = myGUI(root)
		root.geometry('400x320+675+100')
		root.resizable(False,False)
		root.mainloop()

if __name__ == '__main__':
	root = Tkinter.Tk()
	main = myGUI(root)
	root.geometry('400x320+675+100')
	root.resizable(False, False,)
	root.mainloop()
