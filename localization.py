from skimage.io import imread #image reading and writing using imread
from skimage.filters import threshold_otsu # Return threshold value based on Otsu method. 
import matplotlib.pyplot as plt
from __main__ import filepath

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
plt.show()




