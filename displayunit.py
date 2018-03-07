#imports needed
import socket
import time
import tkinter as tk
import _thread

#
imageToDisplay = b'Start'  
imageIsUpdated = False


#Setup of root window for the GUI and the different images 
root = tk.Tk()
root.attributes('-fullscreen',True)

image4 = tk.PhotoImage(file="/home/pi/Desktop/wav/questionmark.gif")
questionlabel = tk.Label(image=image4)
answerlabel = tk.Label(image=image4)

#Try to connect to the server untill successfull
HOST = '192.168.1.34'    # The remote host, 
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try: 
	s.connect((HOST, PORT))

except:
	print("FAILED. Sleep briefly & try again")
	time.sleep(10)

#Display the questionmark on the screen
questionlabel.pack()
root.update()

#Loop of the game 
def receiveThread():
	i=1
	while True:
		global imageToDisplay
		imageToDisplay = s.recv(1024) #receive information on what image to display. 
		print(imageToDisplay.decode())
		global imageIsUpdated
		imageIsUpdated = True
		print(i)
		i+1


try:
   _thread.start_new_thread( receiveThread, ())
except:
   print ("Error: unable to start thread")


while True:
	if imageIsUpdated == True:
		path = '/home/pi/Desktop/wav/%s.gif' % imageToDisplay.decode() #set the path to this desired image
		questionlabel.pack_forget()
		answerlabel.pack_forget()
		#Display the image at the path
		image1 = tk.PhotoImage(file=path) 
		answerlabel = tk.Label(image=image1)
		answerlabel.pack()
		root.update()
		imageIsUpdated = False