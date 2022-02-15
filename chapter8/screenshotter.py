import base64
import win32api as api
import win32con as con
import win32gui as gui
import win32ui as ui

def get_dimensions():
    width = api.GetSystemMetrics(con.SM_CXVIRTUALSCREEN)
    height = api.GetSystemMetrics(con.SM_CYVIRTUALSCREEN)
    left = api.GetSystemMetrics(con.SM_XVIRTUALSCREEN)
    top = api.GetSystemMetrics(con.SM_YVIRTUALSCREEN)
    return (width, height, left, top)

def screenshot(name='screenshot'):
    hdesktop = gui.GetDesktopWindow()
    width, height, left, top = get_dimensions()

    desktop_dc = gui.GetWindowDC(hdesktop)
    img_dc = ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()

    screenshot = ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)
    mem_dc.BitBlt((0,0), (width, height), img_dc, (left, top), con.SRCCOPY)
    screenshot.SaveBitmapFile(mem_dc, f'{name}.bmp')

    mem_dc.DeleteDC()
    gui.DeleteObject(screenshot.GetHandle())

def run():
    screenshot()
    with open('screenshot.bmp') as f:
        img = f.read()
    return img

if __name__ == '__main__':
    screenshot()
