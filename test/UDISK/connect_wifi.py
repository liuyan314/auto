#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST

'''
用例标题:“添加网络”中链接wifi
预置条件
1.系统在主界面
2.清除用户数据
测试步骤：
1.打开应用：settings
2.点击wlan,下滑页面并点击“网络添加”，输入wifi名称和密码，保存，返回
预期结果
1.打开成功且页面在默认最顶端
2.添加WiFi并链接WiFi成功后，返回主页面
'''

class TestScript(unittest.TestCase):  #固定！！！！
    def setUp(self):
        print('返回主界面')
        Common(DUT).goBackHome()

    def step1(self):
        print("步骤1.打开应用：settings")
        Common(DUT).clearUserData(CONST.PACKAGE.SETTINGS) #清除用户数据，保证打开settings后，为默认页面位置（顶部）
        Common(DUT).startActivity(CONST.PKGNAME.SETTINGS)

    def step2(self):
        print("步骤2.链接wifi")
        Common(DUT).clickWhenExist(text=CONST.TEXT.WIFI)
        Common(DUT).clickByText(text=CONST.TEXT.ADD_NETWORK,screeScroll=True)
        Common(DUT).inputText(id=CONST.ID.SSID,text='ChinaNet-r6Y2')
        Common(DUT).clickByText(text=CONST.TEXT.SECURITY_NONE)
        Common(DUT).clickByText(text=CONST.TEXT.WPA_WPA2_PSK)
        Common(DUT).inputText(id=CONST.ID.SSID_PWD,text='liuyan19890314')
        Common(DUT).clickById(id=CONST.ID.OK)
        result=Checkpoint(DUT).checkIfExist(text=CONST.TEXT.CONNECTED)  #检查是否‘已连接’（判断点）
        assert result==True  #判断case结果是否正确

    def test_step(self):
        self.step1()
        self.step2()

    def tearDown(self):
        print("收尾：返回主界面")
        Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
