#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST
from aw.camera import Camera
'''
用例标题:关闭相机里保存地理位置
预置条件
1.系统在主界面
2.清除用户数据
测试步骤：
1.打开应用：camera
2.打开右上角设置，关闭相机里保存地理位置
预期结果
1.打开成功且页面为默认数据
2.关闭相机里保存地理位置成功
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
        print("步骤2.打开设置，关闭显示地理位置")
        Common(DUT).clickById(id=CONST.ID.CAMERA_SETTINGS)
        Camera(DUT).closestorelocation()
        Common(DUT).goBack()



    def test_step(self):
        self.step1()
        self.step2()

    def tearDown(self):
        print("收尾：返回主界面")
        Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
