# Connected component analysis
from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from __main__ import filepath
from Tkinter import *
import localization

def submitIndex():
	global index
	index = E1.get()
	print(index)
	root.destroy()
	
index = 0


# this gets all the connected regions and groups them together
label_image = measure.label(localization.binary_car_image)
print(label_image.shape)
# getting the maximum width, height and minimum width and height that a license plate can be according to the size of image
plate_dimensions = (0.05*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
min_height, max_height, min_width, max_width = plate_dimensions
plate_objects_cordinates = []
plate_like_objects = []
fig, (ax1) = plt.subplots(1)
ax1.imshow(localization.gray_car_image, cmap="gray");

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
        plate_like_objects.append(localization.binary_car_image[min_row:max_row,
                                  min_col:max_col])
        plate_objects_cordinates.append((min_row, min_col,
                                              max_row, max_col))
        rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=2, fill=False)
        ax1.add_patch(rectBorder)
    # let's draw a red rectangle over those regions

if(len(plate_like_objects)>1):
	root = Tk()
	root.title("Number plate index")
	L1 = Label(root, text="Number plate index")
	L1.pack(anchor=N)
	E1 = Entry(root, bd =5)
	E1.pack(anchor=CENTER)
	B1 = Button(root, text="OK", command=submitIndex)
	B1.pack(anchor=S)
	#root.mainloop()
else:	
	global index
	index = 0
plt.show()


