from Module import Module
import codecs
import base64
import string
import random

modules = []

def to_rot_13(flag):
    return codecs.encode(flag, "rot_13")

modules.append(Module("Encode Flag using ROT-13", to_rot_13, []))

def from_rot_13(flag):
    return codecs.decode(flag, "rot_13")

modules.append(Module("Decode Flag using ROT-13", from_rot_13, []))

def to_base64(flag):
    return base64.b64encode(flag.encode())

def from_base64(flag):
    return base64.b64decode(flag.encode())

modules.append(Module("Encode Flag using base64", to_base64, []))

modules.append(Module("Decode Flag using base64", from_base64, []))

def generate_otp(flag):
    asciichars = string.printable
    otp_list = []
    ciphertext_list = []

    for char in flag:
        otp = random.choice(asciichars)
        otp_list.append(otp)
        xor = asciichars.index(char) ^ asciichars.index(otp)
        ciphertext_list.append(asciichars[xor % len(asciichars)])
    otp = "".join(otp_list)
    ciphertext = "".join(ciphertext_list)
    print("OTP: " + otp)
    print("Ciphertext: " + ciphertext)
    return (otp, ciphertext)

modules.append(Module("Encrypt with One-Time-Pad", generate_otp, []))

# This appears to be a non-standard vigenere cipher ...

def encrypt_vigenere(plaintext, key):
    key = key[0]
    key_length = len(key)
    key_as_int = [ord(i.upper()) for i in key]
    plaintext_int = [ord(i.upper()) for i in plaintext]
    ciphertext = ''
    for i in range(len(plaintext_int)):
        if plaintext[i] in string.ascii_letters:
            value = (plaintext_int[i] + key_as_int[i % key_length]) % 26
            if plaintext[i].islower():
                ciphertext += chr(value + 65).lower()
            else:
                ciphertext += chr(value + 65)
        else:
            ciphertext += plaintext[i]
    return ciphertext

def decrypt_vigenere(ciphertext, key):
    key = key[0]
    key_length = len(key)
    key_as_int = [ord(i.upper()) for i in key]
    ciphertext_int = [ord(i.upper()) for i in ciphertext]
    plaintext = ''
    for i in range(len(ciphertext_int)):
        if ciphertext[i] in string.ascii_letters:
            value = (ciphertext_int[i] - key_as_int[i % key_length]) % 26
            if ciphertext[i].islower():
                plaintext += chr(value + 65).lower()
            else:
                plaintext += chr(value + 65)
        else:
            plaintext += ciphertext[i]
    return plaintext

modules.append(Module("Encrypt flag with Vigenere Cipher", encrypt_vigenere, ["Encryption Key (Required)"]))
modules.append(Module("Decrypt flag with Vigenere Cipher", decrypt_vigenere, ["Decryption Key (Required)"]))