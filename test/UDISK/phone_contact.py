#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST

'''
用例标题:在“电话”中查找联系人并打电话
'''


class TestScript(unittest.TestCase):
    # def setUp(self):
    #     print('返回主界面')
    #     Common(DUT).goBackHome()
    #
    # def step1(self):
    #     print("步骤1.打开应用：电话")
    #     Common(DUT).startActivity(CONST.PKGNAME.DIALAR)

    def step2(self):
        print("步骤2.在电话中查找联系人“妈妈”并拨打电话")
        Common(DUT).clickById(id=CONST.ID.RECORDER_CONTACT)
        Common(DUT).inputText(id='com.android.dialer:id/search_view',text='妈妈')
        Common(DUT).clickByText(text='妈妈')



    def test_step(self):
        # self.step1()
        self.step2()

    # def tearDown(self):
    #     print("收尾：返回主界面")
    #     Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
