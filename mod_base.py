from Module import Module
import binascii

modules = []

def string_to_hex(flag):
    return str(binascii.b2a_hex(flag.encode()).decode())

def binary_to_ascii(flag):
    return str(binascii.b2a_uu(flag.encode()).decode())

def hexbin4_binary_to_ascii(flag):
    return str(binascii.b2a_hqx(flag.encode()).decode())

def string_to_decimal(flag):
    return str(int.from_bytes(flag.encode(), 'big'))

def string_to_binary(flag):
    return str(bin(int.from_bytes(flag.encode(), 'big'))).replace('b', '')


modules.append(Module("Convert Flag to Binary", string_to_binary, []))
modules.append(Module("Convert Flag to Decimal", string_to_decimal, []))
modules.append(Module("Convert Flag to Hex", string_to_hex, []))
modules.append(Module("Treat Flag as Binary and Convert to Ascii", binary_to_ascii, []))
modules.append(Module("Treat Flag as Binary and Perform hexbin4 binary-to-ascii translation", hexbin4_binary_to_ascii, []))
