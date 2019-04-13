from Tkinter import *

def submitIndex():
	print(E1.get())

index = 0
root = Tk()
root.title("Number plate index")
L1 = Label(root, text="Number plate index")
L1.pack(anchor=N)
E1 = Entry(root, bd =5)
E1.pack(anchor=CENTER)
B1 = Button(root, text="OK", command=submitIndex)
B1.pack(anchor=S)

root.mainloop()
