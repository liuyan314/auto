#-*- coding:utf-8 -*-
import unittest
import HTMLTestRunner
import os
import time
from test.egg.app.release import *

rootPath = os.path.abspath(os.path.dirname(__file__))
record = time.strftime("%Y-%m-%d_%H-%M-%S")
spath = rootPath+"\\report\\"+"test_"+record
jsonFile="project.json"

def testSuit():
    suite = unittest.TestSuite()
    suite.addTest(ED_17928_Login_with_email_address.TestScript('test_Login_Email'))
    return suite

def toRun():
    with open(rootPath+"\\project.log", 'w+') as f:
        f.write(spath)
    os.makedirs(spath)
    filename = spath + "\\Test_Report.html"
    fp = open(filename, 'wb')
    # runner = unittest.TextTestRunner()
    # runner.run(testSuit())
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title="AutoTestReport", description='AutoTest')
    runner.run(testSuit())
    fp.close()
    return filename

if __name__=="__main__":
    toRun()