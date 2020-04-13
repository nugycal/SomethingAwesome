from Module import Module
from zipfile import ZipFile
import tempfile
from os import access, R_OK


modules = []

def zip_files(files):
    temp, filename = tempfile.mkstemp()
    filename += ".zip"
    zip = ZipFile(filename, "w")

    file_list = files.split("|")
    file_list = [f.strip() for f in file_list]

    for f in file_list:
        if access(f, R_OK):
            try:
                zip.write(f)
            except Exception as e:
                print(e)
                continue
        else:
            print(f"Unable to access file {f}.")
            continue
    zip.close()
    return filename

def zip_files_existing(f, options):
    if len(options) == 1 or options[1].strip() == "":
        zip = ZipFile(options[0], "a")
    else:
        zip = ZipFile(options[0], "a", pwd=options[1])
    try:
        zip.write(f)
    except Exception as e:
        print(e)
    zip.close()
    return f


def add_comment(zip, comment):
    zipfile = ZipFile(zip, "a")
    zipfile.comment = comment.encode()
    zipfile.close()
    return zip

def add_comment_flag(flag, zip):
    return add_comment(zip[0], flag)

def add_comment_generated(zip, text):
    return add_comment(zip, text[0])

def add_password(zip, passwd):
    zipfile = ZipFile(zip, "a")
    zipfile.setpassword(passwd)
    zipfile.close()
    return zip

def add_password_flag(flag, zip):
    return add_password(zip[0], flag)

def add_password_gen(zip, text):
    return add_password(zip, text[0])

modules.append(Module("Add Generated File to new Zip Archive", zip_files, []))
modules.append(Module("Add Generated File to existing Zip Archive", zip_files_existing, ["Absolute Path to Zip Archive (Required)", "Password (leave blank if none)"]))
modules.append(Module("Add flag as comment to existing zip archive", add_comment_flag, ["Absolute Path to Zip Archive (Required)"]))
modules.append(Module("Add comment to generated zip archive", add_comment_generated, ["Comment (cannot excede 65535 bytes, required)"]))
modules.append(Module("Add flag as password to existing zip archive", add_password_gen, ["Absolute Path to Zip Archive (Required)"]))
modules.append(Module("Add password to generated zip archive", add_password_flag, ["Password (Required)"]))
