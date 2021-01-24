#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST
import random

'''
用例标题:新建联系人
预置条件
1.系统在主界面
2.清除用户数据
测试步骤：
1.打开应用：信息
2.给10086发送短信，内容：9个字母+1个随机数字
预期结果
2.发送短信成功
'''


class TestScript(unittest.TestCase):
    # def setUp(self):
    #     print('返回主界面')
    #     Common(DUT).goBackHome()
    #
    def step1(self):
        print("步骤1.打开应用：MMS")
        Common(DUT).startActivity(CONST.PKGNAME.MMS)
    def step2(self):
        print("步骤2.给10086发送短信，内容：9个字母+1个随机数字")
        Common(DUT).clickById(id=CONST.ID.CREATE_MMS)
        Common(DUT).inputText(id=CONST.ID.RECIPIENT_EDITOR,text='10086')
        Common(DUT).inputText(id=CONST.ID.INPUT_MMS, text='HOWAREYOU'+str(random.randint(0, 10)))
        # Common(DUT).clickById(id=CONST.ID.SEND_MMS)

    def test_step(self):
        self.step1()
        self.step2()

    # def tearDown(self):
    #     print("收尾：返回主界面")
    #     Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
