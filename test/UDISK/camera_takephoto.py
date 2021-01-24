#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST
from aw.camera import Camera

'''
用例标题:相机拍一张带美颜的自拍照
预置条件
1.系统在主界面
2.清除用户数据
测试步骤：
1.打开应用：camera
2.切换为前置摄像头，进行拍照
预期结果
1.打开成功且页面为默认数据
2.摄像头切换成功，且相机拍一张带美颜的自拍照成功
'''


class TestScript(unittest.TestCase):
    def setUp(self):
        print('返回主界面')
        Common(DUT).goBackHome()

    def step1(self):
        print("步骤1.打开应用：camera")
        Common(DUT).clearUserData(CONST.PACKAGE.CAMERA)
        Common(DUT).startActivity(CONST.PKGNAME.CAMERA)

    def step2(self):
        print("步骤2.前置摄像头打开中度美颜自拍并查看")
        Common(DUT).clickById(id=CONST.ID.FRONT_BACK_SWITCHER)
        Camera(DUT).beautyface()
        Common(DUT).clickById(id=CONST.ID.SHUTTER_BUTTON)
        Common(DUT).clickById(id=CONST.ID.PREVIEW_THUMB)


    def test_step(self):
        self.step1()
        self.step2()

    def tearDown(self):
        print("收尾：返回主界面")
        Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
