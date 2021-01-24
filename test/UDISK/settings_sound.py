#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST

'''
用例标题:设置中调节音量大小
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
        print("步骤2.调节音量大小")
        Common(DUT).swipeByRelativeCoordinates(0.7,0.7,0.7,0.4)  #滑动相对坐标
        # Common(DUT).swipe(1034,1651,1034,470) #滑动绝对坐标
        Common(DUT).clickWhenExist(text=CONST.TEXT.VOICE)
        # Common(DUT).click(1180, 460)
        # Common(DUT).click(430,460)    # Common(DUT).volumeDown()



    def test_step(self):
        # self.step1()
        self.step2()

    # def tearDown(self):
    #     print("收尾：返回主界面")
    #     Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
