import os
from aw import *
from aw.common import Common
from uiautomator import Device
from logger import Logger
from aw.CONST import *

class Camera(Common):

    def __init__(self, sn=None):
        # global d
        self.d = Device(sn)
        self.sn = sn
        self.record = time.strftime('%Y-%m-%d_%H-%M-%S')


    def closestorelocation(self):
        if self.d(text='保存地理位置').right(resourceId='org.codeaurora.snapcam:id/right_image').checked==False:
            self.d(text='保存地理位置').right(resourceId='org.codeaurora.snapcam:id/right_image').click()


    def beautyface(self):
        Common(DUT).clickById(id='org.codeaurora.snapcam:id/ts_makeup_switcher')
        Common(DUT).clickByText(text='继续')
        Common(DUT).clickByText(text='中')


if __name__ == "__main__":
    unittest.main()
