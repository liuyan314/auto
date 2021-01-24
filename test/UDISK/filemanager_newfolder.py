#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST
from aw.filemanager import Filemanager

'''
用例标题：文件管理器创建文件并进行文件夹搜索功能
'''

class TestScript(unittest.TestCase):
    def setUp(self):
        print('返回主界面')
        Common(DUT).goBack(4)

    def step1(self):
        print("步骤1.打开应用：文件管理器")
        Common(DUT).startActivity(CONST.PKGNAME.FILEMANAGER)

    def step2(self):
        print("步骤2.文文件管理器创建文件")
        Common(DUT).clickByText(text=CONST.TEXT.FOLDER)
        Common(DUT).clickByText(text=CONST.TEXT.INTERNAL_STORAGE)
        Common(DUT).clicktopright()
        Common(DUT).clickByText(text='新建文件夹')
        Common(DUT).inputText(id='com.cloudminds.filemanager:id/text',text='nihao')
        Common(DUT).clickByText(text=CONST.TEXT.FILEMANAGER_NEWFOLDER_SURE)

    def step3(self):
        print("步骤3.文件夹搜索功能")
        Common(DUT).clickById(id=CONST.ID.FILEMANAGER_NEWFOLDER_SEARCH)
        Common(DUT).inputText(id='com.cloudminds.filemanager:id/et_search', text='nihao')
        Common(DUT).clickById(id='com.cloudminds.filemanager:id/iv_search')

    def test_step(self):
        self.step1()
        self.step2()
        self.step3()

    def tearDown(self):
        print("收尾：返回主界面")
        Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
