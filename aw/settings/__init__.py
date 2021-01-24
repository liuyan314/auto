import os
from aw import *
from aw.common import Common
from uiautomator import Device
from logger import Logger
from aw.CONST import *

class Settings(Common):

    def __init__(self, sn=None):
        # global d
        self.d = Device(sn)
        self.sn = sn
        self.record = time.strftime('%Y-%m-%d_%H-%M-%S')

    def autorotate_screen(self):
        if self.d(text='自动旋转屏幕').right(resourceId='android:id/switch_widget').checked==True:
            self.d(text='自动旋转屏幕').right(resourceId='android:id/switch_widget').click()


if __name__ == "__main__":
    unittest.main()
