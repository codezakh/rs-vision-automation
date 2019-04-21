import yaml
from yaml import Loader 
import subprocess
from dataclasses import dataclass
import pyscreenshot as pyss 
import py_prtscn

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
im.show()