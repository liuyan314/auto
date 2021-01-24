#-*- coding:utf-8 -*-
from aw import *
#from aw.CONST import *
from aw import CONST
from aw.contact import Contact

'''
用例标题:新建联系人并拨打电话
预置条件
1.系统在主界面
2.清除用户数据
测试步骤：
1.打开应用：contacts
2.点击新建图标，添加名字（name）及电话号码（phone）后，保存并拨打电话
预期结果
1.打开成功且页面在默认最顶端
2.添加成功，并显示正确，并拨打电话成功
'''


class TestScript(unittest.TestCase):
    # def setUp(self):
    #     print('返回主界面')
    #     Common(DUT).goBackHome()

    # def step1(self):
    #     print("步骤1.打开应用：contacts")
    #     Common(DUT).startActivity(CONST.PKGNAME.CONTACTS)

    def step2(self):
        print("步骤2.新建联系人")
        Contact(DUT).contactadd()


        # Common(DUT).clickById(id=CONST.ID.AAD_CONTACTS)
        # Common(DUT).inputTextByText(text=CONST.TEXT.CONTACTS_NAME,text_str='移动号码')
        # Common(DUT).inputTextByText(text=CONST.TEXT.CONTACTS_PHONE,text_str='10086')
        # Common(DUT).clickById(id=CONST.ID.SAVE_CONTACTS)
        # Common(DUT).goBack()
        # Common(DUT).clickByText(text=CONST.TEXT.CONTACTS_ALL)
        # Common(DUT).clickByText(text="老哥")
        # Common(DUT).clickById(id=CONST.ID.CONTACTS_DIALER)


    def test_step(self):
        # self.step1()
        self.step2()

    # def tearDown(self):
    #     print("收尾：返回主界面")
    #     Common(DUT).goBackHome()

if __name__ == "__main__":
    unittest.main()
