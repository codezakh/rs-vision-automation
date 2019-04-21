import yaml
from yaml import Loader 
import subprocess
from dataclasses import dataclass
import pyscreenshot as pyss 
import py_prtscn
import os
from PIL import Image
import pyautogui as agui
import random
from collections import namedtuple

source_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(source_dir, 'data')

Point = namedtuple('Point', ['x', 'y'])

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
        return py_prtscn.grab_screen(*self.get_bounding_box())

    def locate(self, img_to_locate):
        self_screenshot = self.take_screenshot()
        left, top, width, height = agui.locate(img_to_locate, self_screenshot, confidence=0.7)
        located_bbox = BoundingBox(
            left=left + self.x,
            top=top + self.y,
            width=width,
            height=height
        )

        return located_bbox

    def locate_all(self, img_to_locate):
        self_screenshot = self.take_screenshot()
        all_located = agui.locateAll(img_to_locate, self_screenshot, confidence=0.6, grayscale=True)

        located_bboxes = [
            BoundingBox(
                left=left + self.x,
                top=top + self.y,
                width=width,
                height=height 
            ) for left, top, width, height in all_located
        ]

        return located_bboxes

@dataclass
class BoundingBox:
    left: int
    top: int
    width: int
    height: int

    @property
    def centroid(self):
        return Point(x=self.left + self.width / 2, y=self.top + self.height / 2)

    def move_to_center(self):
        jittered_center = jitter(self.centroid)
        return agui.moveTo(jittered_center.x, jittered_center.y, duration=0.5, tween=agui.easeInElastic)

def jitter(point, x_radius=10, y_radius=10):
        x_jittered = point.x + random.uniform(-x_radius, x_radius)
        y_jittered = point.y + random.uniform(-y_radius, y_radius)
        return Point(x=x_jittered, y=y_jittered)



window_geometry_raw = subprocess.check_output('./get_window_geometry.sh', shell=True).decode('utf-8').strip()
window_geometry = yaml.load(window_geometry_raw, Loader=Loader)

window = Window(**window_geometry)
im = window.take_screenshot()
im.save(os.path.join(data_dir, 'screenshot.png'))

knife_image = Image.open(os.path.join(data_dir, 'Knife.png'))
unstrung_maple_bow_image = Image.open(os.path.join(data_dir, 'MapleLongbowUnstrung.png'))

# left, top, width, height = agui.locate(knife_image, im)
# agui.moveTo(window.x + 2 + left, window.y + top + 3, duration=1, tween=agui.easeInElastic)
# agui.click()

knife_bbox = window.locate(knife_image)
knife_bbox.move_to_center()
print(len(window.locate_all(unstrung_maple_bow_image)))
#agui.moveTo(x=knife_bbox.centroid.x, y=knife_bbox.centroid.y, duration=2, tween=agui.easeInElastic)