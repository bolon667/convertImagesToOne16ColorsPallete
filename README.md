# Convert images to One 16bit palette. Python script.
Python script, which combines palette of images. It's useful for SGDK, for example, you want to use 1 palette for all entity.

## How to use

1. Put images in **imagesIn** folder
2. Run **convertImagesToOne16BitPalette.py**
3. Result will be in **imagesOut** folder

## How it works

1. Script creating combines all your images into one atlas.
2. Reducing palette of atlas
3. Cropping images from atlas to get images back.
