#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST
from aw.filemanager import Filemanager

'''
用例标题：文件管理器中取消收藏的图片
'''

class TestScript(unittest.TestCase):
    def setUp(self):
        print('返回主界面')
        Common(DUT).goBack(4)

    def step1(self):
        print("步骤1.打开应用：文件管理器")
        Common(DUT).startActivity(CONST.PKGNAME.FILEMANAGER)

    def step2(self):
        print("步骤2.文件管理器中添加图片收藏后再取消收藏的图片")
        Filemanager(DUT).addtofavorites()
        Filemanager(DUT).removetofavorites()

    def test_step(self):
        self.step1()
        self.step2()

    def tearDown(self):
        print("收尾：返回主界面")
        Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
