import os,sys
import time
import json
from uiautomator import Device,device
from aw.common import Common
# from aw.settings import Setting
from aw.CONST import LOOP
from aw import CONST
# from aw.luCiNet import *
# from aw.QQMusic import *
from aw.checkpoint import Checkpoint
# from aw.initProject import *
# from aw.Libratone import *
from datetime import datetime
import run
try:
    import HTMLTestRunner
except Exception as e:
    print("Import HTMLTestRunner error")
import unittest

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__),os.path.pardir))
resourcePath = rootPath+"\\resource\\"

def _DATA():
    with open(rootPath+"\\project.json","r") as f:
        return json.load(f)
DATA=_DATA()

def setDeviceSn(device="DUT"):
    dut=DATA["device"][device]["sn"]
    Sn=dut if dut != "None" else None
    return Sn

DUT=setDeviceSn("DUT")
# SUBDUT1=setDeviceSn("DUT")