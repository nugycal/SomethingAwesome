from Module import Module
from PIL import Image, ImageDraw
import requests
import shutil
import tempfile
import piexif

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

def hide_text_in_exif(image, options):
    text = options[0]
    im = get_image(image)
    path = tempfile.mkstemp()[1] + ".jpg"
    im.save(path, exif=piexif.dump({"0th":{piexif.ImageIFD.Make: text.encode('utf-8')}}))
    im.close()
    return path


def hide_in_exif(flag, options):
    image = options[0]
    return hide_text_in_exif(image, flag)

modules.append(Module("Hide Flag in Image EXIF data", hide_in_exif, ["Absolute Path to Image (Required)"]))
modules.append(Module("Hide Text in Already Generated Image EXIF data", hide_text_in_exif, ["Text (Required)"]))
