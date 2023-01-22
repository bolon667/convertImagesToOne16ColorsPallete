import glob
from PIL import Image
import libimagequant as liq
import sys
import math

def start():
    #reduce pallete in png images
    png_path = "./imagesIn/*"
    cut_data, save_path = combine_images(png_path)
    reduce_png_pallete(save_path)
    uncombine_images(save_path, cut_data)
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

def uncombine_images(path, cut_data_arr):
    combined_img = Image.open(path)
    for cut_data in cut_data_arr:
        rect = cut_data["rect"]
        file_name = cut_data["file_name"]
        temp_img = combined_img.crop(rect)
        temp_img.save("imagesOut/" + file_name)
        

def combine_images(path):
    print(path)
    png_list = glob.glob(path)
    
    cut_positions = []
    spritesheet_size_x = 0
    spritesheet_size_y = 0
    #Getting spritesheet size
    for png_path in png_list:
        #Getting frame size
        tempImg = Image.open(png_path).convert('RGBA')
        frame_size = (tempImg.width, tempImg.height)
        
        cur_x = spritesheet_size_x
        
        png_name = png_path[png_path.rfind("\\")+1:]
        cut_data = {
                "file_name": png_name,
                "rect": (cur_x, 0, cur_x+tempImg.width, tempImg.height),
        }
        cut_positions.append(cut_data)
        spritesheet_size_x += tempImg.width
        if(tempImg.height > spritesheet_size_y):
            spritesheet_size_y = tempImg.height
        tempImg.close()
    
  
    #Creating spritesheet
    imgSpritesheet = Image.new(mode="RGBA", size=(spritesheet_size_x, spritesheet_size_y))
    cur_x = 0
    cur_y = 0
    
    for png_path in png_list:
        tempImg = Image.open(png_path).convert('RGBA')
        
        imgSpritesheet.paste(tempImg, (cur_x, cur_y))
        tempImg.close()
        cur_x += tempImg.width
    
    save_path = f"./imagesOut/animation-{int(spritesheet_size_x/8)}_{int(spritesheet_size_y/8)}_5.png"
    imgSpritesheet.save(save_path)
    imgSpritesheet.close()
    return cut_positions, save_path
   
    
start()