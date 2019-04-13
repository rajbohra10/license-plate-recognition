from Tkinter import *
from tkFileDialog import *
from PIL import Image, ImageTk
from skimage.io import imread #image reading and writing using imread
from skimage.filters import threshold_otsu # Return threshold value based on Otsu method. 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage import measure
from skimage.measure import regionprops
import numpy as np
from skimage.transform import resize
from sklearn.externals import joblib
import os
import ntpath
# CONSTANTS
VERY_LIGHT_GRAY = "#989898"
DARK_GRAY = "#282828"
MEDIUM_GRAY = "#424242"
TEXT_COLOR = "white"

# GLOBAL VARIABLES
filename = ""
filepath = ""

window = Tk()
window.title("License plate recognition")

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
	
	
def localization():
	#filename = raw_input("Enter file name")
	car_image = imread(filepath, as_gray=True)
	# it should be a 2 dimensional array
	# prints the size of the image
	print(car_image.shape)
	# the next line is not compulsory however, a grey scale pixel
	# in skimage ranges between 0 & 1. multiplying it with 255
	# will make it range between 0 & 255 (something we can relate better with)
	# Otsu's method is used to convert grayscale image to binary
	gray_car_image = car_image * 255
	fig, (ax1, ax2) = plt.subplots(1, 2)
	ax1.imshow(gray_car_image, cmap="gray")
	threshold_value = threshold_otsu(gray_car_image)
	# binary_car_image will have true value for value greater than otsu's threshold
	binary_car_image = gray_car_image > threshold_value
	ax2.imshow(binary_car_image, cmap="gray")
	window.destroy()
	plt.show()
	cca(gray_car_image, binary_car_image)
	
def cca(gray_car_image, binary_car_image):
	# connected component analysis
	# this gets all the connected regions and groups them together

	label_image = measure.label(binary_car_image)
	# getting the maximum width, height and minimum width and height that a license plate can be according to the size of image
	plate_dimensions = (0.08*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
	min_height, max_height, min_width, max_width = plate_dimensions
	plate_objects_cordinates = []
	plate_like_objects = []
	fig, (ax1) = plt.subplots(1)
	ax1.imshow(gray_car_image, cmap="gray");
	print"Hello world"
	# regionprops creates a list of properties of all the labelled regions
	for region in regionprops(label_image):
	    if region.area < 50:
		#if the region is so small then it's likely not a license plate, skip to next iteration
		continue

	    # the bounding box coordinates
	    min_row, min_col, max_row, max_col = region.bbox
	    region_height = max_row - min_row
	    region_width = max_col - min_col
	    # ensuring that the region identified satisfies the condition of a typical license plate
	    if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
		plate_like_objects.append(binary_car_image[min_row:max_row,
		                          min_col:max_col])
		plate_objects_cordinates.append((min_row, min_col,
		                                      max_row, max_col))
		rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=2, fill=False)
		ax1.add_patch(rectBorder)
		#plt.show()
	    # let's draw a red rectangle over those regions
	print"Hello world"	
	plt.show() 
	segmentation(plate_like_objects)
	

def segmentation(plate_like_objects):
	index = 0
	print(len(plate_like_objects))
	if(len(plate_like_objects)>1):
		root = Tk()
		root.title("Number plate index")
		root.mainloop()
	else:
		index = 0
		
	license_plate = np.invert(plate_like_objects[index])
		
	labelled_plate = measure.label(license_plate)

	#fig, ax1 = plt.subplots(1)
	#ax1.imshow(license_plate, cmap="gray")
	# the next two lines is based on the assumptions that the width of
	# a license plate should be between 5% and 15% of the license plate,
	# and height should be between 35% and 60%
	# this will eliminate some
	character_dimensions = (0.35*license_plate.shape[0], 0.60*license_plate.shape[0], 0.05*license_plate.shape[1], 0.15*license_plate.shape[1])
	min_height, max_height, min_width, max_width = character_dimensions

	characters = []
	counter=0
	column_list = []
	for regions in regionprops(labelled_plate):
	    y0, x0, y1, x1 = regions.bbox
	    region_height = y1 - y0
	    region_width = x1 - x0

	    if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
		roi = license_plate[y0:y1, x0:x1]

		# draw a red bordered rectangle over the character.
		rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red",
		                               linewidth=2, fill=False)
		#ax1.add_patch(rect_border)

		# resize the characters to 20X20 and then append each character into the characters list
		resized_char = resize(roi, (20, 20))
		characters.append(resized_char)

		# this is just to keep track of the arrangement of the characters
		column_list.append(x0)
	plt.show()
	prediction(characters, column_list)
	
	
def prediction(characters, column_list):
	current_dir = os.path.dirname(os.path.realpath(__file__))
	model_dir = os.path.join(current_dir, 'models/svc/svc.pkl')
	model = joblib.load(model_dir)

	classification_result = []
	for each_character in characters:
	    # converts it to a 1D array
	    each_character = each_character.reshape(1, -1);
	    result = model.predict(each_character)
	    classification_result.append(result)

	print(classification_result)

	plate_string = ''
	for eachPredict in classification_result:
	    plate_string += eachPredict[0]

	print(plate_string)

	# it's possible the characters are wrongly arranged
	# since that's a possibility, the column_list will be
	# used to sort the letters in the right order

	column_list_copy = column_list[:]
	column_list.sort()
	rightplate_string = ''
	for each in column_list:
	    rightplate_string += plate_string[column_list_copy.index(each)]

	print(rightplate_string)
	
	
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
filemenu.add_command(label="Run", command=localization)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.config()
window.config(menu=menubar)

window.mainloop()

