# Convert images to One 16Colors palette. Python script.
Python script, which combines palette of images. It's useful for SGDK, for example, you want to use 1 palette for all entity.

## How to use

1. Put images in **imagesIn** folder
2. Run **convertImagesToOne16BitPalette.py**
3. Result will be in **imagesOut** folder

## Installing dependisies

From program folder, run this command in cmd

`pip install -r requirements.txt`

## How it works

1. Script combines all your images into one atlas.
2. Reducing palette of atlas
3. Cropping images from atlas to get images back.

## Additionaly

You also can use:

- **convertImages.py** to reduce palette to 16 colors
- **resizeImages.py** to change size of images (needs rewriting for your needs).
- **createAnimation.py** to create spriteSheet from frames. You should give appropriate names to images, like 1.png, 2.png... and so on.
