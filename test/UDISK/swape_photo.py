#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST

'''
用例标题:长按删除图库中的一张图片
预置条件
1.系统在主界面
2.清除用户数据
测试步骤：
1.打开应用：CAMERA
2.选择滑动照片
预期结果
1.打开成功且页面为默认数据
2.左右滑动查看照片成功
'''


class TestScript(unittest.TestCase):
    def setUp(self):
        print('返回主界面')
        Common(DUT).goBackHome()

    def step1(self):
        print("步骤1.打开应用：CAMERA")
        Common(DUT).clearUserData(CONST.PACKAGE.CAMERA)
        Common(DUT).startActivity(CONST.PKGNAME.CAMERA)

    def step2(self):
        print("步骤2.滑动图片")
        Common(DUT).clickById(id=CONST.ID.PREVIEW_THUMB)
        Common(DUT).swipe(900,600,400,600)

    def test_step(self):
        self.step1()
        self.step2()

    def tearDown(self):
        print("收尾：返回主界面")
        Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
