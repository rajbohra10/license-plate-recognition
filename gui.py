from Tkinter import *
from tkFileDialog import *
from PIL import Image, ImageTk
import ntpath
# CONSTANTS
VERY_LIGHT_GRAY = "#989898"
DARK_GRAY = "#282828"
MEDIUM_GRAY = "#424242"
TEXT_COLOR = "white"

window = Tk()
window.title("License plate recognition")

filename = ""
filepath = ""
def importFile():
	global filename, filepath
	filepath = askopenfilename() # show an "Open" dialog box and return the path to the selected file
	print(filepath)
	filename = ntpath.basename(filepath) 
	image = Image.open(filepath)
	#image = ImageTk.resize((800, 800), Image.ANTIALIAS)
	print("filename is "+filename)
	photo = ImageTk.PhotoImage(image)
	canvas.create_image(50, 10, image=photo, anchor=NW)
	canvas.update()
	canvas.mainloop()
	
	
def runPrediction():
	window.destroy()
	import prediction

def showResult(rightplate_string):
	root = Tk()
	root.title("Result")
	print"final result"+rightplate_string
	var = StringVar()
	label = Label( root, textvariable=var, relief=RAISED )
	label.config(font=("Courier", 44))
	var.set(rightplate_string)
	label.pack()
	root.mainloop()
	
#button = Button(window, text='START', width=25, command=runPrediction)	
#button.pack(anchor=E)

frame=Frame(window,width=500,height=500)
frame.pack(anchor=CENTER)

canvas = Canvas(frame, width=500, height=500, background=VERY_LIGHT_GRAY, scrollregion=(0,0,1200,1200))
hbar=Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(width=500,height=500)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)

menubar = Menu(window)
'''file menu'''
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Import image", command=importFile)
filemenu.add_command(label="Run", command=runPrediction)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.config()
window.config(menu=menubar)

window.mainloop()

