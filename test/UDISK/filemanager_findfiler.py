#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST

'''
用例标题：文件管理器添加并寻找apk
'''

class TestScript(unittest.TestCase):
    # def setUp(self):
    #     print('返回主界面')
    #     Common(DUT).goBack(4)
    #
    # def step1(self):
    #     print("步骤1.打开应用：文件管理器")
    #     Common(DUT).startActivity(CONST.PKGNAME.FILEMANAGER)

    def step2(self):
        print("步骤2.添加并寻找apk")
        '''
        1.push文件，把放在电脑里的文件放在手机里
        '''
        Common(DUT).pushFile(fileName='apk/123.apk',toPath='/sdcard/') #添加apk
        Common(DUT).clickById(id=CONST.ID.FILEMANAGER_SEARCH)
        Common(DUT).inputTextByText(text=CONST.TEXT.FILEMANAGER_RESEARCH, text_str='123.apk')
        Common(DUT).clickById(id=CONST.ID.SEARCH)
        '''
        2.pull文件，把手机里的文件放在电脑里
        '''
        Common(DUT).pullFile(fromPath='/sdcard/QQyinle_647.apk', toPath='D:\workspace\A\\resource\\video')

    def test_step(self):
        # self.step1()
        self.step2()

    # def tearDown(self):
    #     print("收尾：返回主界面")
    #     Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
