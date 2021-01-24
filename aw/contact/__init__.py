import os
from aw import *
from aw.common import Common
from uiautomator import Device
from logger import Logger
from aw.CONST import *

class Contact(Common):

    def contactadd(self):
        self.clickById(id=CONST.ID.AAD_CONTACTS)
        self.inputTextByText(text=CONST.TEXT.CONTACTS_NAME,text_str='刘岩')
        self.inputTextByText(text=CONST.TEXT.CONTACTS_PHONE,text_str='1111')
        self.clickById(id=CONST.ID.SAVE_CONTACTS)

    # def contactadd(self,id):
    #     self.clickById(id)
    #
    # def addname(self,text_str,text="姓名"):
    #     self.inputTextByText(text_str)
    #
    # def addphone(self,text_str,text="电话"):
    #     self.inputTextByText(text_str)
    #
    # def addsave(self,id):
    #     self.clickById(id)

if __name__ == "__main__":
    unittest.main()
