import yaml
from yaml import Loader 
import subprocess
from dataclasses import dataclass
import pyscreenshot as pyss 
import py_prtscn
import os
from PIL import Image
import pyautogui as agui

source_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(source_dir, 'data')

@dataclass(frozen=True)
class Window:
    x: int
    y: int
    windowId: int
    width: int
    height: int

    def get_bounding_box(self):
        return self.x, self.y, self.x + self.width, self.y + self.height

    def take_screenshot(self):
        #return pyss.grab(bbox=self.get_bounding_box())
        return py_prtscn.grab_screen(*self.get_bounding_box())



window_geometry_raw = subprocess.check_output('./get_window_geometry.sh', shell=True).decode('utf-8').strip()
window_geometry = yaml.load(window_geometry_raw, Loader=Loader)

window = Window(**window_geometry)
im = window.take_screenshot()

knife_image = Image.open(os.path.join(data_dir, 'Knife.png'))

left, top, width, height = agui.locate(knife_image, im)
agui.moveTo(window.x + 2 + left, window.y + top + 3, duration=1, tween=agui.easeInElastic)
agui.click()