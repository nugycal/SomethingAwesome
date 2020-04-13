from Module import Module
from PIL import Image, ImageDraw
import stepic
import requests
import shutil
import tempfile

# These methods are derived from this article:
# https://www.geeksforgeeks.org/image-based-steganography-using-python/

modules = []

def get_image(path):
    image = ""
    if "http" in path:
        try:
            image = requests.get(path, stream=True)
            if image.status_code != 200:
                print(f"Error: Received HTTP Status Code {image.status_code} for requested resource {path}")
                raise Exception
            temp, name = tempfile.mkstemp()
            name += ".png"
            file = open(name, "wb")
            image.raw.decode_content = True
            shutil.copyfileobj(image.raw, file)
            file.close()
            f = Image.open(name, "r")
            temp, name = tempfile.mkstemp()
            name += ".jpg"
            f.save(name, "JPEG")
            f.close()
            file = Image.open(name, "r")
            image = file
        except ValueError as e:
            print(e)
            exit(1)
    else:
        try:
            image = Image.open(path, "r")
        except Exception as e:
            print(e)
            exit(1)
    return image

def encode_enc(image, data):
    return stepic.encode(image, data.encode())

def hide(image, data):
    old_file = image
    image = get_image(image)
    new = image.copy()
    new = encode_enc(new, data)
    
    file, name = tempfile.mkstemp()
    ext = old_file.split(".")
    if len(ext) == 1:
        ext = "PNG"
    else:
        ext = ext[-1]
    new.save(name, ext)
    return name

def hide_flag_in_image(data, image):
    image = image[0]
    old_file = image
    image = get_image(image)
    new = image.copy()
    new = encode_enc(new, data)
    
    file, name = tempfile.mkstemp()
    ext = old_file.split(".")
    if len(ext) == 1:
        ext = "PNG"
    else:
        ext = ext[-1]
    if ext.lower() == "jpg":
        ext = "JPEG"
    new.save(name, ext)
    return name

modules.append(Module("Hide Flag in Image", hide_flag_in_image, ["Path to Image (Required)"]))

def hide_text_in_image(image, text):
    text = text[0]
    return hide(image, text)

modules.append(Module("Hide Text in Already Generated Image", hide_text_in_image, ["Text to Insert (Required)"]))

def gen_image(text, options):
    color = 'black'
    font_color = 3
    if len(options) == 2:
        width, height = options
    elif len(options) == 3:
        width, height, color = options
    elif len(options) == 4:
        width, height, color, font_color = options
    else:
        print("error: invalid options!")
        return text

    width = int(width)
    height = int(height)

    if width < 10 or height < 10:
        print("error: too small")
        return text

    if font_color == 3:
        if "dark" in color or "black" in color:
            font_color = "white"
        else:
            font_color = "black"

    img = Image.new('RGB', (width, height), color = color)
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill = font_color)
    
    no, file = tempfile.mkstemp()
    img.save(file, "PNG")
    return file

def gen_image_and_hide(flag, options):
    if len(options) < 1:
        print("invalid options!")
        return flag
    else:
        image_path = gen_image(options[0], options[1:])
        return hide_flag_in_image(flag, [image_path])


modules.append(Module("Hide Flag in Image Generated from Text", gen_image_and_hide, ["Text (Required)", "Width (Required)", "Height (Required)", "Background color", "Font Color"]))
modules.append(Module("Generate Image from Flag", gen_image, ["Width (Required)", "Height (Required)", "Background color", "Font Color"]))
