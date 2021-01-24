#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST

'''
用例标题:拨打10086，通话5s挂断
测试步骤：
1.打开应用：电话
2.拨打10086，通话5s挂断
预期结果
2.拨打成功，并且在通话5s挂断
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
        print("步骤2.拨打10086，通话5s挂断")
        Common(DUT).clickById(id=CONST.ID.DIALAR_KEYBORD)
        Common(DUT).clickByText(text=CONST.TEXT.TEXT_1)
        Common(DUT).clickByText(text=CONST.TEXT.TEXT_0)
        Common(DUT).clickByText(text=CONST.TEXT.TEXT_0)
        # Common(DUT).clickByText(text=CONST.TEXT.TEXT_8)
        Common(DUT).clickByText(text=CONST.TEXT.TEXT_6)
        Common(DUT).clickById(id=CONST.ID.DIALAR_BUTTON)



    def test_step(self):
        # self.step1()
        self.step2()

    # def tearDown(self):
    #     print("收尾：返回主界面")
    #     Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
