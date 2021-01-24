#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST

'''
用例标题:系统语言切换为英文
'''

class TestScript(unittest.TestCase):  #固定！！！！
    # def setUp(self):
    #     print('返回主界面')
    #     Common(DUT).goBackHome()
    #
    # def step1(self):
    #     print("步骤1.打开应用：settings")
    #     Common(DUT).clearUserData(CONST.PACKAGE.SETTINGS) #清除用户数据，保证打开settings后，为默认页面位置（顶部）
    #     Common(DUT).startActivity(CONST.PKGNAME.SETTINGS)

    def step2(self):
        print("步骤2.系统语言从中文切换为英文")
        Common(DUT).swipeToBottom()
        Common(DUT).clickWhenExist(text=CONST.TEXT.LAUNAGE)
        Common(DUT).clickByText(text=CONST.TEXT.LAUNAGE_launage)
        Common(DUT).drag(1350,700,1350,365)
        result=Checkpoint(DUT).checkIfExist(text="Language preferences")  #检查版本号是否为‘A1-901.1r.96’（判断点）
        assert result==True  #判断case结果是否正确

    def test_step(self):
        # self.step1()
        self.step2()

    # def tearDown(self):
    #     print("收尾：返回主界面")
    #     Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
