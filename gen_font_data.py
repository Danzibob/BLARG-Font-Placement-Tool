import os, json
from PIL import Image
from random import choice

LETTER_FOLDER = "Letter Images"
GIF_FOLDER = "imgs"

letter_coords = {}

def XY2I(x,y):
    return y*48 + x

# Create image templates for each file
for filename in os.listdir(LETTER_FOLDER):
    if filename == "_tjImage.png": continue
    name = ".".join(filename.split(".")[:-1])
    print(name)
    cap, letter = name.split("_")
    if cap:
        letter = letter.upper()
    else:
        letter = letter.lower()
    im = Image.open(LETTER_FOLDER + "/" + filename)
    pixels = [0]*(48*44)
    for x in range(48):
        for y in range(44):
            px = im.getpixel((x,y))
            # print(px)
            #if px == (255,255,255,255) or px == (210,175,111,255) or px == (255,255,255) or px == 1:
            if px == (0,0,0) or px == (0,0,0,255):
                pixels[XY2I(x,y)] = 1
                # Fuzzify 1 px in each direction:
    
    
    letter_coords[letter] = pixels
with open("fontBase.json", "w+") as file:
    json.dump(letter_coords, file)