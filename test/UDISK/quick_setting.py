#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST
from aw.quicksetting import Quicksetting
import random

'''
用例标题:快速设置-打开手电筒
'''


class TestScript(unittest.TestCase):
    # def setUp(self):
    #     print('返回主界面')
    #     Common(DUT).goBackHome()
    #
    # def step1(self):
    #     print("步骤1.打开快速设置栏")
    #     Common(DUT).openQuicksetting()

    def step2(self):
        print("步骤2.点开手电筒")
        Quicksetting(DUT).openflashlight()

    def test_step(self):
        # self.step1()
        self.step2()

    # def tearDown(self):
    #     print("收尾：返回主界面")
    #     Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
