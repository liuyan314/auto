import os
from aw import *
from aw.common import Common
from uiautomator import Device
from logger import Logger
from aw.CONST import *

class Quicksetting(Common):

    def __init__(self, sn=None):
        # global d
        self.d = Device(sn)
        self.sn = sn
        self.record = time.strftime('%Y-%m-%d_%H-%M-%S')


    def openflashlight(self):
        if self.d(text='手电筒').up(resourceId='android:id/icon').checked==False:
            self.d(text='手电筒').up(resourceId='android:id/icon').click()


if __name__ == "__main__":
    unittest.main()
