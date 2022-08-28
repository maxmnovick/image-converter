# image-converter.py
# convert image format from webp to jpg so it can be resized
# resize image by containing it in box with same aspect ratio 
# and then expanding it with border/background fill color

from PIL import Image, ImageOps

import glob, re

set_side_length = 2048 # final image will be square with this desired side length, in px
print("Set Side Length: " + str(set_side_length) + "px")

# for all images in staging area
# folder created with new and ready images to convert
# remove the images from this folder after so they are not reconverted next run
# or change the folder this program is looking for. give this program (as input) a different folder to look for.

# how do we know the name of the file to open? 
# in this case, we name it in format <sku>-<type>.webp
# is there a way to open all files in a folder, one by one, so we do not need filename?
# yes with Glob library
images = glob.glob("product-images/new/*.webp")

for image in images:

    im_name = re.sub("product-images/new/","",image) # remove first part of filepath
    im_name = re.sub("\.webp","",im_name) # remove end/last part of filepath
    #print("im_name: " + im_name)

    print("\n===Open Image: " + im_name + "===\n")

    im = Image.open(image) #Image.open("../Data/product-images/example.webp")

    # get image dimensions so we can see if size needs to increase or decrease
    init_width, init_height = im.size
    print("init_width: " + str(init_width))
    print("init_height: " + str(init_height))
    print()

    final_width = init_width
    final_height = init_height

    print("\n===Contain Image===\n")
    im_with_border = ImageOps.contain(im, (set_side_length, set_side_length), Image.Resampling.LANCZOS) # this is to make sure the image gets resized properly

    # if image square then we do not need border
    if init_width == init_height:
        final_width = final_height = set_side_length

    elif init_width > init_height:
        final_width = set_side_length # larger side is 2048px

        size_change_factor = init_width / final_width
        final_height = round(init_height / size_change_factor)

    elif init_width < init_height:
        final_height = set_side_length

        size_change_factor = init_height / final_height
        final_width = round(init_width / size_change_factor)

    print()

    # if image width below 2048px, we do not necessarily want to increase width directly to 2048px,
    # because the height could then go above 2048px, which is not allowed
    # so if the height would increase above 2048px, then we need to check height before changing width
    # if the height would not go above 2048px by increasing width to 2048, then we still want to make width 2048 and fill space above and below image with fill color

    print("final_width no border: " + str(final_width))
    print("final_height no border: " + str(final_height))

    # either one or both of these borders will be 0 bc the larger side will be equal to set side length
    width_border = round(abs(final_width - set_side_length) / 2)
    height_border = round(abs(final_height - set_side_length) / 2)
    print("width_border: " + str(width_border))
    print("height_border: " + str(height_border))

    im_with_border = ImageOps.expand(im_with_border, border=(width_border, height_border), fill='black')
    
    im_with_border.show() # for testing

    print("final_width: " + str(final_width+2*width_border))
    print("final_height: " + str(final_height+2*height_border))

    # save the converted and resized image
    im_path = "product-images/upload/" + im_name + ".jpg"
    im_with_border.save(im_path, im_with_border.format) # see if we can resize in webp format then we do not need to convert