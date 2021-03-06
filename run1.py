#-*- coding:utf-8 -*-
'''
Created on 2017.06

@author: chubaoliang
'''
import time,os,sys,json
import unittest
import HTMLTestRunner
from aw.CONST import IP
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.header import Header

rootPath = os.path.abspath(os.path.dirname(__file__))
record = time.strftime("%Y-%m-%d_%H-%M-%S")
spath = rootPath+"\\report\\"+"test_"+record
jsonFile="project.json"

def getModuleList():
    moduleList=[]
    with open(rootPath+"\\test1.txt") as f:
        for line in f.readlines():
            line=line.split()[0]
            line=line.split(".")[0]
            if line[0] !="#" and len(line) != 0:
                moduleList.append(line)
    print("计划执行用例 :"+str(len(moduleList))+"条")
    return moduleList

def testSuit():
    suite = unittest.TestSuite()
    for m in getModuleList():
        if "\\" in m:
            m=m.replace("\\",".")
            testModule = __import__(m,{},{},["test"])
        else:
            testModule = __import__("test.libratone." + m, {}, {}, ["test"])
        suite.addTest(testModule.TestScript('test_step'))
    return suite

def changeConfig(A, B):
    f= open(rootPath+"\\"+jsonFile,"r")
    s=f.read()
#     s=s.replace("\"screencap\":\"no\"","\"screencap\":\"yes\"")
    s=s.replace(A, B)
    f.close()
    p=open(jsonFile,"w+")
    p.write(s)
    p.close()

def toRun(cfgFileName="project"):
    os.popen("adb connect %s:5555"%IP.IP)
    with open(rootPath+"\\project.log", 'w+') as f:
        f.write(spath)
    os.makedirs(spath)
    print ("Report saved to :"+spath)
    filename = spath+"\\Test_Report.html"
    fp = open(filename,'wb')
    print(cfgFileName+" is running")
    runner = unittest.TextTestRunner()
    runner.run(testSuit())
    # runner=HTMLTestRunner.HTMLTestRunner(stream=fp,title="AutoTestReport",description='AutoTest')
    # runner.run(testSuit())
    fp.close()
    return filename

if __name__=="__main__":
    newfile=toRun()