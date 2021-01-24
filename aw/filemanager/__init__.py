import os
from aw import *
from aw.common import Common
from uiautomator import Device
from logger import Logger
from aw.CONST import *

class Filemanager(Common):

    def __init__(self, sn=None):
        # global d
        self.d = Device(sn)
        self.sn = sn
        self.record = time.strftime('%Y-%m-%d_%H-%M-%S')

    def addtofavorites(self):
        '''
        1.图片添加为收藏
        '''
        Common(DUT).clickByText(text='分类')
        Common(DUT).clickByText(text='图片')
        Common(DUT).long_clickById(index=4, id=CONST.ID.FILEMANAGER_IMAGE)
        Common(DUT).clicktopright()
        Common(DUT).clickByText(text='添加收藏')

    def removetofavorites(self):
        '''
        2.取消收藏的图片
        '''
        Common(DUT).goHome()
        Common(DUT).startActivity(CONST.PKGNAME.FILEMANAGER)
        Common(DUT).clickByText(text='收藏')
        Common(DUT).long_clickById(index=0, id='com.cloudminds.filemanager:id/favorite_list')
        Common(DUT).clicktopright()
        Common(DUT).clickByText(text='取消收藏')

if __name__ == "__main__":
    unittest.main()
