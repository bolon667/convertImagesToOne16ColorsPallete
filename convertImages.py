import glob
from PIL import Image
import libimagequant as liq
import sys
import math

def convert_images():
    #reduce pallete in png images
    path = "./imagesIn/*"
    print(path)
    png_list = glob.glob(path)
    for png_file in png_list:
        png_path = png_file.replace("\\","/")
        file_format = png_path[png_path.rfind(".")+1:]
        supported_formats = ['png', 'bmp']
        if file_format not in supported_formats:
            print("Error: Unsupported image format\nYou shoud use 'png' or 'bmp'")
            continue
        
        resized_path = resize_image(png_path)
        reduce_png_pallete(resized_path) 
    print("All images reduced to 16 colors")


def reduce_png_pallete(image_url):
    MAX_SIZE = (320, 224)
    print("Reduce image pallete")
    
        
    imgSource = Image.open(image_url).convert('RGBA')
    
    width = imgSource.width
    height = imgSource.height
    input_rgba_pixels = imgSource.tobytes()

    # Use libimagequant to make a palette for the RGBA pixels

    attr = liq.Attr()
    attr.max_colors = 16
    input_image = attr.create_rgba(input_rgba_pixels, width, height, 0)

    result = input_image.quantize(attr)

    # Use libimagequant to make new image pixels from the palette

    result.dithering_level = 0

    raw_8bit_pixels = result.remap_image(input_image)
    palette = result.get_palette()

    # Save converted pixels as a PNG file
    # This uses the Pillow library for PNG writing (not part of libimagequant)
    imgSource = Image.frombytes('P', (width, height), raw_8bit_pixels)

    palette_data = []
    for color in palette:
        palette_data.append(color.r)
        palette_data.append(color.g)
        palette_data.append(color.b)
    imgSource.putpalette(palette_data)
    
    output_png_file_path = image_url.replace("/images/", "/imagesOut/")
    imgSource.save(output_png_file_path)

    print('Written reduce palette version: ' + output_png_file_path)
    
def resize_image(image_url):
    #original 700x500 to sega 320x224
    imgSource = Image.open(image_url).convert('RGBA')
    width = imgSource.width
    height = imgSource.height
    #Get appropriate sega resolution of sprites
    newRes = (int(width*0.457), int(height*0.448))
    #New must be able to divide on 8
    newRes = (math.ceil(newRes[0]/8)*8, math.ceil(newRes[1]/8)*8)

    img = Image.new(mode="RGBA", size=newRes)
    imgSource.thumbnail(newRes)
    
    img.paste(imgSource)
    
    output_png_file_path = image_url.replace("/imagesIn/", "/imagesOut/")
    print('Written rezied version: ' + output_png_file_path)
    img.save(output_png_file_path)
    
    return output_png_file_path
   
    
convert_images()