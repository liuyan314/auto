# -*- coding:utf-8 -*-
'''
Created on:2017.06
#author:chubaoliang

'''
import datetime
import json
import os
import serial
import subprocess
import time
import wave
import inspect
from datetime import datetime

import VideoCapture
#from PIL import Image
#from pyaudio import PyAudio, paInt16

from aw import CONST
from logger import Logger
from uiautomator import Device

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

# define of params
CHUNK = 2000
RATE = 48000
CHANNELS = 1
SAMPWIDTH = 2
# record time
TIME = 10


def config():
    jsonFile = "project.json"
    with open(rootPath + "\\" + jsonFile, "r") as f:
        config = json.load(f)
    return config


def step(func):
    def wraper(*args, **kwargs):
        func(*args, **kwargs)
        time.sleep(0.5)
        _screenShot()

    return wraper


def _screenShot():
    with open(rootPath + '\\project.log', 'r') as f:
        savePath = f.readline().strip()
    if config()['log_config']['screencap'] == 'yes':
        record = time.strftime('%Y-%m-%d_%H-%M-%S')
        imagepath = '/data/local/tmp/' + record + '.png'
        sn = config()['device']['DUT']['sn']
        if sn == 'None':
            subprocess.Popen('adb shell screencap -p ' + imagepath, shell=True).wait()
            subprocess.Popen('adb pull ' + imagepath + ' ' + savePath + '\\' + record + '.png', shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            print("<a href=\"" + savePath + "\\" + record + ".png\"" + " target=\"_blank\">点击查看截图</a>")
            subprocess.Popen('adb shell rm ' + imagepath).wait()
        else:
            subprocess.Popen('adb -s %s shell screencap -p ' % sn + imagepath, shell=True).wait()
            subprocess.Popen('adb -s %s pull ' % sn + imagepath + ' ' + savePath + '\\' + record + '.png', shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            print("<a href=\"" + savePath + "\\" + record + ".png\"" + " target=\"_blank\">点击查看截图</a>")
            subprocess.Popen('adb -s %s shell rm ' % sn + imagepath, shell=True).wait()


class Common(object):
    def __init__(self, sn=None):
        global d
        d = Device(sn)
        self.sn = sn
        self.record = time.strftime('%Y-%m-%d_%H-%M-%S')

    def screenShot(self):
        with open(rootPath + "\\project.log", "r") as f:
            savePath = f.readline().strip()
        imagepath = "/data/local/tmp/" + self.record + ".png"
        if self.sn == None:
            os.popen("adb shell screencap -p " + imagepath)
            os.popen("adb pull " + imagepath + " " + savePath + "\\" + self.record + ".png")
            #             Logger.info("截图保存至："+self.savePath+"\\"+self.record+".png")
            os.popen("adb shell rm " + imagepath)
        else:
            os.popen("adb -s %s shell screencap -p " % self.sn + imagepath)
            os.popen("adb -s %s pull " % self.sn + imagepath + " " + savePath + "\\" + self.record + ".png")
            os.popen("adb -s %s shell rm " % self.sn + imagepath)

    def shell(self, cmd):
        return self.adbCmd('shell ' + cmd)

    def adbCmd(self, cmd):
        if self.sn == None:
            subprocess.Popen('adb ' + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            Logger.info('adb ' + cmd)
        else:
            subprocess.Popen('adb -s %s ' % self.sn + cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE).communicate()
            Logger.info('adb -s %s ' % self.sn + cmd)

    def wait(self, seconds):
        Logger.info("wait %d seconds" % seconds)
        time.sleep(seconds)

    @step
    def startActivity(self, activity_name, timeOut=2):
        self.shell("am start -n " + activity_name)
        time.sleep(timeOut)
        if activity_name == "com.tencent.qqmusic/.activity.AppStarterActivity":
            self.clickWhenExist(text="暂不升级")
            self.clickWhenExist(resourceId="com.tencent.qqmusic:id/c95")

    @step
    def click(self, x, y):
        '''
        1. 点击绝对坐标
        '''
        d.click(x, y)
        self.wait(1)

    @step
    def clickObject(self, **keyargs):
        d(**keyargs).click()

    @step
    def click_relative(self, a, b, waitTime=1):
        '''
        1. 点击相对坐标
        '''
        x, y = self.getScreenSize()
        self.click(a * x, b * y)
        self.wait(waitTime)

    @step
    def long_click(self, x, y):
        '''
        1. 长点击
        '''
        d.long_click(x, y)

    @step
    def clickByText(self, text, index=0, screeScroll=False, direction="up_down", timeout=20, waitTime=2):
        x, y = self.getScreenSize()
        if screeScroll == True:
            startTime = time.time()
            while time.time() - startTime < timeout:
                if d(text=text, instance=index).exists:
                    d(text=text, instance=index).click()
                    Logger.info("click text: " + text)
                    time.sleep(1)
                    break
                else:
                    if direction == "up_down":
                        d.swipe(x * 0.5, y * 0.8, x * 0.5, y * 0.5, 40)
                    if direction == "left_right":
                        d.swipe(x * 0.8, y * 0.5, x * 0.4, y * 0.5, 40)
                    time.sleep(waitTime)
        else:
            d(text=text, instance=index).click()
            Logger.info("click text: " + text)
            self.wait(1)

    @step
    def long_clickByText(self, text, index=0, screeScroll=False, direction="up_down", timeout=20, waitTime=2):
        x, y = self.getScreenSize()
        if screeScroll == True:
            startTime = time.time()
            while time.time() - startTime < timeout:
                if d(text=text, instance=index).exists:
                    d(text=text, instance=index).long_click()
                    Logger.info("click text: " + text)
                    time.sleep(1)
                    break
                else:
                    if direction == "up_down":
                        d.swipe(x * 0.5, y * 0.8, x * 0.5, y * 0.5, 40)
                    if direction == "left_right":
                        d.swipe(x * 0.8, y * 0.5, x * 0.4, y * 0.5, 40)
                    time.sleep(waitTime)
        else:
            d(text=text, instance=index).long_click()
            Logger.info("click text: " + text)
            self.wait(1)

    @step
    def clickById(self, id, index=0, screeScroll=False, direction="up_down", timeout=10):
        '''
        '''
        if screeScroll == True:
            startTime = time.time()
            while time.time() - startTime < timeout:
                if d(resourceId=id, instance=index).exists:
                    d(resourceId=id, instance=index).click()
                    Logger.info("click id: " + id)
                    time.sleep(2)
                    break
                else:
                    if direction == "up_down":
                        d.swipe(500, 800, 500, 200, 40)
                    if direction == "left_right":
                        d.swipe(700, 500, 100, 500, 40)
                    time.sleep(1)
        else:
            d(resourceId=id, instance=index).click()
            Logger.info("click id: " + id)
            time.sleep(1)


    @step
    # 通话挂断功能；
    def clickMatchId(self, id, index=0, screeScroll=False, direction="up_down", timeout=10):
        '''
        '''
        if screeScroll == True:
            startTime = time.time()
            while time.time() - startTime < timeout:
                if d(resourceIdMatches=id, instance=index).exists:
                    d(resourceIdMatches=id, instance=index).click()
                    Logger.info("click id: " + id)
                    time.sleep(2)
                    break
                else:
                    if direction == "up_down":
                        d.swipe(500, 800, 500, 200, 40)
                    if direction == "left_right":
                        d.swipe(700, 500, 100, 500, 40)
                    time.sleep(1)
        else:
            d(resourceIdMatches=id, instance=index).click()
            Logger.info("click id: " + id)
            time.sleep(1)

    @step
    def long_clickById(self, id, index=0, screeScroll=False, timeout=10):
        '''
        1.长按控件
        '''
        if screeScroll == True:
            startTime = time.time()
            while time.time() - startTime < timeout:
                if d(resourceId=id, instance=index).exists:
                    d(resourceId=id, instance=index).long_click()
                    Logger.info("long click id: " + id)
                    time.sleep(2)
                    break
                else:
                    d.swipe(500, 800, 500, 200, 50)
                    time.sleep(1)
        else:
            d(resourceId=id, instance=index).long_click()
            Logger.info("long click id: " + id)
            time.sleep(1)


    @step
    def clicktopright(self):
        '''
        点击屏幕右上角
        '''
        self.click(1356,252)


    @step
    def switchWidget(self, status, resourceId):
        '''
        status: "true", "false",为当前控件状态，非期望状态
        '''
        _dict = {
            "关闭": "true",
            "开启": "false",
            "true": "true",
            "false": "false"
        }
        if d(checked=_dict[status], resourceId=resourceId).exists:
            d(resourceId=resourceId).click()
        else:
            Logger.info("当前开关状态为：" + status)

    @step
    def switchWighetByIndex(self, status, index=0, resourceId="amigo:id/amigo_switchWidget"):
        '''
        1,根据控件数目，转换控件，顺序 0,1,2,3...
        '''
        _dic = {
            "关闭": True,
            "开启": False
        }
        if d(resourceId=resourceId)[index].info["checked"] == _dic[status]:
            d(resourceId=resourceId)[index].click()

    def goHome(self, times=1):
        for i in range(times):
            d.press("home")
        Logger.info("返回Home桌面")

    def goBack(self, times=1):
        for i in range(times):
            d.press("back")
        Logger.info("按Back键返回")

    # @step
    def goBackHome(self):
        self.goBack(4)
        self.goHome()

    @step
    def pressRecent(self):
        d.press("recent")
        Logger.info("按recent键")

    def clearRecentApp(self):
        '''
        1.清理后台应用
        '''
        self.pressRecent()
        self.wait(1)
        d(resourceId="com.android.systemui:id/clear_all_recents_image_button").click()  # device：HUAWEI-MATE7
        self.wait(2)
        Logger.info("清理后台应用")

    @step
    def volumeUp(self):
        d.press("volume_up")

    @step
    def volumeDown(self):
        d.press("volume_down")

    @step
    def openCamera(self, toDo="picture", times=2):
        self.startActivity("com.android.camera/.CameraLauncher")
        self.clickWhenExist(className="android.widget.Button")
        self.clickWhenExist(text="继续")
        if toDo == "picture":
            for i in range(times):
                d(resourceId="com.android.camera:id/shutter_button_icon").click()
                time.sleep(2)

    def putSettings(self, field, modul, mode):
        self.shell("settings put " + field + " " + modul + " " + mode)

    def installApk(self, name, mode=None):
        '''
        1.安装应用
        '''
        if mode == None:
            path = rootPath + "\\resource\\apk\\" + name
            self.adbCmd("install " + path)
        else:
            path = rootPath + "\\resource\\apk\\" + name
            self.adbCmd("install " + mode + " install " + path)

    def uninstallApp(self, pkgName):
        '''
        1.卸载应用
        '''
        if self.sn == None:
            os.popen("adb uninstall " + pkgName)
            Logger.info("adb uninstall " + pkgName)
        else:
            os.popen("adb -s %s uninstall " % self.sn + pkgName)
            Logger.info("adb -s %s uninstall " % self.sn + pkgName)

    def allowAppPermissions(self):
        self.launchSettings()
        self.clickByText("应用管理", screeScroll=True)
        self.clickByText("应用权限", screeScroll=True)
        time.sleep(1)
        d.click(653, 93)
        self.clickByText("全部信任")
        self.goBack(5)
        self.goHome()

    def closeRotateScreen(self):
        '''
        1.关闭屏幕旋转
        '''
        d.freeze_rotation()

    def launchSettings(self):
        '''
        1.打开设置
        '''
        self.startActivity("com.android.settings/.GnSettingsTabActivity")

    def dialNum(self, numList):
        '''
        KEYCODE_HOME=3;
        KEYCODE_BACK=4;
        KEYCODE_CALL=5;
        KEYCODE_ENDCALL=6;
        KEYCODE_0=7;
        KEYCODE_1=8;
        KEYCODE_2=9;
        KEYCODE_3=10;
        KEYCODE_4=11;
        KEYCODE_5=12;
        KEYCODE_6=13;
        KEYCODE_7=14;
        KEYCODE_8=15;
        KEYCODE_9=16;
        KEYCODE_STAR=17;
        KEYCODE_POUND=18;
        '''
        KEYCODE_DIC = {
            "0": 7,
            "1": 8,
            "2": 9,
            "3": 10,
            "4": 11,
            "5": 12,
            "6": 13,
            "7": 14,
            "8": 15,
            "9": 16,
            "*": 17,
            "#": 18,
        }
        for i in numList:
            num = KEYCODE_DIC[i]
            self.shell("input keyevent " + str(num))
            time.sleep(0.5)

    def setTimeByUI(self):
        localTime = str(datetime.datetime.now())
        localTime = localTime.replace("-", ":")
        localTime = localTime.replace(" ", ":")
        localTime = localTime.split(":")
        print(localTime)
        _min = localTime[4]
        _hour = localTime[3]
        _day = localTime[2]
        _month = localTime[1]
        _year = localTime[0]
        self.launchSettings()
        self.clickByText("更多设置", screeScroll=True)
        self.clickByText("日期和时间", screeScroll=True)
        self.clickByText("设置时间")
        count = 60
        while count > 0:
            print(_min)
            if d.exists(text=_min):
                break
            else:
                d.swipe(466, 1006, 466, 876, 50)
                count = count - 1
                time.sleep(1)
        d.swipe(466, 1006, 466, 876, 50)
        d.swipe(466, 1006, 466, 876, 50)
        time.sleep(1)
        count1 = 24
        while count1 > 0:
            print(_hour)
            if d.exists(text=_hour):
                break
            else:
                d.swipe(253, 1006, 253, 876, 50)
                count1 = count1 - 1
                time.sleep(1)
        self.clickByText("确定")
        self.clickByText("设置日期")
        count2 = 31
        while count2 > 0:
            if d.exists(text=_day):
                break
            else:
                d.swipe(566, 1006, 566, 876, 50)
                count2 = count2 - 1
                time.sleep(1)
        count3 = 12
        while count3 > 0:
            if d.exists(text=_month):
                break
            else:
                d.swipe(359, 1006, 359, 876, 50)
                count3 = count3 - 1
                time.sleep(1)
        count4 = 5
        while count4 > 0:
            if d.exists(text=_year):
                break
            else:
                d.swipe(153, 1006, 153, 876, 50)
                count4 = count4 - 1
                time.sleep(1)
        count5 = 10
        while count5 > 0:
            if d.exists(text=_year):
                break
            else:
                d.swipe(153, 876, 153, 1006, 50)
                count5 = count5 - 1
                time.sleep(1)
        self.clickByText("确定")
        Logger.info("时间设置成功")

    def clickWhenExist(self, **keyargs):
        '''
        1.点击符合条件的控件
        '''
        if d(**keyargs).exists:
            self.clickObject(**keyargs)
            k = list(keyargs.keys())[0]
            v = keyargs[k]
            Logger.info("click %s : %s " % (k, v))
            time.sleep(0.5)
        else:
            Logger.info("widget not exist.")
            pass

    @step
    def lockScreen(self):
        '''
        1.按power键锁定屏幕
        '''
        d.press("power")
        Logger.info("锁屏")
        #         self.shell("input keyevent 26")

    @step
    def unlockScreen(self):
        '''
        1.滑动解锁手机
        '''

        self.wakeUp()
        self.swipe(350, 950, 350, 200, 30)
        Logger.info("解锁屏幕")

    def copyFile(self, filepath, toPath):
        self.adbCmd("push " + filepath + " " + toPath)

                # if self.sn==None:
                #     os.popen("adb push "+filepath+" "+toPath)
                # else:
                #     os.popen("adb -s %s push "%self.sn+filepath+" "+toPath)

    def pushFile(self, fileName, toPath):
        if self.sn == None:
            os.popen("adb push " + rootPath + "\\resource\\" + fileName + " " + toPath)
        else:
            os.popen("adb -s %s push " % self.sn + rootPath + "\\resource\\" + fileName + " " + toPath)

    def pullFile(self, fromPath, toPath):
        if self.sn == None:
            os.popen("adb pull " + fromPath + " " + toPath)
        else:
            os.popen("adb -s %s pull " % self.sn + fromPath + " " + toPath)

    # def inputText(self, text):
    #     '''
    #     1.输入文本（中文除外）
    #     '''
    #     self.shell("input text " + text)
    #     self.shell("input keyevent 66")

    def swipe(self, sx, sy, ex, ey, steps=10):
        '''
        1.滑动屏幕
        '''
        d.swipe(sx=sx, sy=sy, ex=ex, ey=ey, steps=steps)
        self.wait(0.5)

    def swipeByRelativeCoordinates(self, SX, SY, EX, EY, steps=10):
        '''
        1.根据相对坐标滑动屏幕
        pamars：
        SX:起始x轴的相对坐标
        SY:起始y轴的相对坐标
        EX:终点x轴的相对坐标
        EY:终点y轴的相对坐标
        steps:滑屏幅度,数字越大,滑的越慢,数字越小,滑动越快
        方法使用,例：swipeByRelativeCoordinates(0.5,0.8,0.5,0.3),解释：横坐标在屏幕50%,纵坐标从80%位置滑到30%位置
        '''
        x, y = self.getScreenSize()
        d.swipe(sx=SX * x, sy=SY * y, ex=EX * x, ey=EY * y, steps=steps)
        self.wait(1)

    def swipeToTop(self):
        '''
        1.滑动到屏幕顶端
        '''
        d.swipe(500, 300, 500, 1000, 2)
        self.wait(2)

    def swipeToBottom(self):
        '''
        1.滑动到屏幕底部
        '''
        d.swipe(500, 800, 500, 300, 2)
        self.wait(2)

    def drag(self, sx, sy, ex, ey, steps=10):
        '''
        1.拖动
        '''
        d.drag(sx=sx, sy=sy, ex=ex, ey=ey, steps=steps)

    def setDefaultIme(self, ime):
        '''
        1.设置默认输入法
        '''
        # adb shell ime list -s 可查看当前手机的输入法列表
        self.shell("ime set " + ime)

    def wakeUp(self):
        '''
        1.唤醒手机
        '''
        d.wakeup()

    def clearUserData(self, pkgName):
        '''
        1.清除应用数据
        '''
        self.shell("pm clear " + pkgName)

    def forceCloseApp(self, pkgName):
        '''
                1.清除应用数据
                '''
        self.shell("am force-stop " + pkgName)

    def getGnVersion(self):
        '''
        1.获取手机软件版本号
        '''
        sn = self.sn if self.sn != None else "None"
        GnVersion = os.popen(
            "adb -s %s shell getprop ro.gn.gnznvernumber" % sn).read() if sn != "None" else os.popen(
            "adb shell getprop ro.gn.gnznvernumber").read()
        GnVersion = GnVersion.strip()
        return GnVersion

    def getScreenSize(self):
        '''
        1.获取屏幕大小
        '''
        sn = self.sn if self.sn != None else "None"
        SS = os.popen(
            "adb -s %s shell dumpsys window displays | findstr init=" % sn).read() if sn != "None" else os.popen(
            "adb shell dumpsys window displays | findstr init=").read()
        SS = SS.strip().split(" ")
        SS = SS[0].split("=")
        SS = SS[1].split("x")
        X = SS[0]
        Y = SS[1]
        return int(X), int(Y)

    def openNotification(self):
        d.open.notification()

    def openQuicksetting(self):
        d.open.quick_settings()
        x, y = self.getScreenSize()
        self.swipe(0.5 * x, 0.1 * y, 0.5 * x, 0.5 * y, 20)

    def clickScreenCenter(self):
        x, y = self.getScreenSize()
        self.click(0.5 * x, 0.5 * y)

    def setAirplaneMode(self, mode):
        '''
        1, 设置飞行模式, True为开启,False为关闭
        '''
        mode_dic = {
            "开启": "false",
            "关闭": "true"
        }
        self.launchSettings()
        self.clickByText("更多连接")
        self.switchWidget(mode_dic[mode], "amigo:id/amigo_switchWidget")
        self.goBackHome()
        #         if mode==True:
        #             self.shell("settings put global airplane_mode_on 1")
        #         if mode==False:
        #             self.shell("settings put global airplane_mode_on 0")

    def doubleClick(self, x, y):
        '''
        1,双击坐标点
        '''
        d.double_click(x, y)

    def setScreenTimeout(self, timeout):
        '''
        1,设置屏幕休眠时间
        '''
        _dic = {
            "30min": 1800000,
            "10min": 600000,
            "5min": 300000,
            "2min": 120000,
            "1min": 60000,
            "30sec": 30000,
            "15sec": 15000
        }
        self.shell("settings put system screen_off_timeout " + str(_dic[timeout]))

    def inputText(self, id, text, index=0):
        d(resourceId=id, instance=index).set_text(text)

    def inputTextByText(self, text, text_str, index=0):
        d(text=text, instance=index).set_text(text_str)

    def exists(self, **keyargs):
        return d(**keyargs).exists

    def nohupTest(self, jarFile, testCase):
        self.uninstallApp("com.github.uiautomator")
        self.pushFile("jar\\" + jarFile, "/data/local/tmp/" + jarFile)
        if self.sn == None:
            cmd = "adb shell uiautomator runtest " + jarFile + " --nohup -c com.power.test.testCase#" + testCase
        else:
            cmd = "adb -s %s " % self.sn + "shell uiautomator runtest " + jarFile + " --nohup -c com.power.test.testCase#" + testCase
        print(cmd)
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)

    def clickWatcher(self, *args, **keyargs):
        watcherName = str(*args)
        d.watcher(watcherName).when(**keyargs).click(**keyargs)
        return watcherName
        #         print(d.watchers)
        #         print(d.watchers.triggered)

    def removeWatcher(self, name):
        d.watcher(name).remove()
        print(d.watchers)

    def takePhotoByCamera(self, devnum=0):
        '''
        param devnum:int
            VideoCapture enumerates the available video capture devices
            on your system. If you have more than one device, specify
            the desired one here. The device number starts from 0.
        '''
        picPath = os.path.join(rootPath, 'report')
        timeNow = time.strftime("%Y-%m-%d_%H-%M-%S")
        camera = VideoCapture.Device(devnum=devnum)
        camera.saveSnapshot(picPath + "\\" + '%s.png' % timeNow, quality=75, timestamp=0, boldfont=1)
        # print(picPath+"\\"+'%s.png'%timeNow)
        return picPath + "\\" + '%s.png' % timeNow

    def getTextValueWithID(self, id):
        '''
        param id:id
        通过已知控件id，来获取控件文本信息
        '''
        return d(resourceId=id).info["text"]

    def getIdValueWithText(self, text):
        '''
        param text:text
        通过已知控件text，来获取控件id信息
        '''
        return d(text=text).info["resourceId"]

    def calSecondsValue(self, end, start):
        """
        function：计算时间差（分，秒级别）
        param
        start:开始时间
        end:结束时间

        """
        return ((datetime.strptime(end, '%M:%S')) - (datetime.strptime(start, '%M:%S'))).seconds

    def createCatchLogcatBat(self):
        sn = config()['device']['DUT']['sn']
        # print("sn is %s"%sn)
        toolsPath = os.path.join(rootPath, "tools")
        batDemoPath = os.path.join(toolsPath, "Logcat_demo.txt")
        logcat_bat_name = "catchLogcat.bat"
        logcat_name = "logcat.txt"
        if os.path.exists(os.path.join(toolsPath, logcat_bat_name)):
            os.remove(os.path.join(toolsPath, logcat_bat_name))
        content = open(batDemoPath).read()
        with open(os.path.join(toolsPath, logcat_bat_name), "w") as f:
            f.write(content % (sn, toolsPath, logcat_name))

    def createCloseLogcatBat(self):
        toolsPath = os.path.join(rootPath, "tools")
        batDemoPath = os.path.join(toolsPath, "closeLogcat_demo.txt")
        close_logcat_bat_name = "closeLogcat.bat"
        if os.path.exists(os.path.join(toolsPath, close_logcat_bat_name)):
            os.remove(os.path.join(toolsPath, close_logcat_bat_name))
        content = open(batDemoPath).read()
        with open(os.path.join(toolsPath, close_logcat_bat_name), "w") as f:
            f.write(content % (toolsPath))

    def closeLogcat(self, device):
        sn = config()['device'][device]['sn']
        res = os.popen('adb -s %s shell \"ps | grep logcat\"' % sn).read()
        if res == "":
            return None
        elif res != "":
            res = res.split()
            if len(res) > 10:
                os.system('adb -s %s shell kill %s' % (sn, res[10]))
                os.system('adb -s %s shell kill %s' % (sn, res[1]))
            elif len(res) < 10:
                os.system('adb -s %s shell kill %s' % (sn, res[1]))
            else:
                pass
        else:
            pass

    def runLogcatBat(self, batName):
        '''
        function:run bat conmand
        :param
        batName:The bat name,one of  catchLogcat.bat/closeLogcat.bat
        '''
        batPath = os.path.join(rootPath, "tools", batName)
        subprocess.Popen(batPath)

    def getSongNameFromLogcat(self):
        '''
        function:通过logcat获取歌曲名字
        :return:返回一个歌曲名字
        '''
        logPath = os.path.join(rootPath, "tools", "logcat.txt")
        contentList = []
        f = open(logPath, mode='r', encoding="utf-8", errors='ignore').read()
        for line in "".join(f.split("\r\n")).split("\n\n"):
            if '\"title\"' in line:
                contentList.append(line)
        # print(contentList)
        try:
            songName = contentList[-1].split("\"")[-2]
            Logger.info("get the song name is %s " % songName)
            return songName
        except Exception as e:
            Logger.info("can not get the song name")
            print(e)

    def connectLibProduct(self):
        sn = config()['device']['DUT']['sn']
        # print(sn)
        resp = os.popen("adb connect %s:%s" % (sn, "5555")).read().strip()
        # print(resp)
        if resp in ["connected to %s:%s" % (sn, "5555"), "already connected to %s:%s" % (sn, "5555")]:
            print("The equipment %s is connected" % sn)
            return True
        else:
            print("The equipment %s is not connected,May equipment not start." % sn)
            return False

    def switchUdiskMode(self, bat="Udisk.bat", timeOut=10):
        batPath = os.path.join(rootPath, "tools", bat)
        subprocess.Popen(batPath).wait()
        Logger.info("Switch Udisk mode")
        time.sleep(timeOut)

    def switchLineinMode(self, bat="Linein.bat", timeOut=10):
        batPath = os.path.join(rootPath, "tools", bat)
        subprocess.Popen(batPath).wait()
        Logger.info("Switch Linein mode")
        time.sleep(timeOut)

    def switchPowerMode(self, bat="Power.bat", timeOut=10):
        batPath = os.path.join(rootPath, "tools", bat)
        subprocess.Popen(batPath).wait()
        Logger.info("Switch Power mode")
        time.sleep(timeOut)

    def waitWidget(self, timeout=5, **keyargs):
        '''
        wait widget and is exists
        :param timeout:
        :param keyargs:
        :return:
        '''
        startTime = time.time()
        print("startTime == " + str(startTime))
        while time.time() - startTime < timeout:
            if d(**keyargs).exists:
                k = list(keyargs.keys())[0]
                v = keyargs[k]
                Logger.info("click %s : %s " % (k, v))
                break
            else:
                time.sleep(1)

    def waitWidgetNotExists(self, timeout=5, **keyargs):
        '''
        wait widget and is exists
        :param timeout:
        :param keyargs:
        :return:
        '''
        startTime = time.time()
        while time.time() - startTime < timeout:
            if d(**keyargs).exists:
                time.sleep(1)
            else:
                break

    def getLayout(self, **keyargs):
        layout_list = []
        if self.exists(**keyargs):
            info = d(**keyargs).info
            left = info["bounds"]["left"]
            top = info["bounds"]["top"]
            right = info["bounds"]["right"]
            bottom = info["bounds"]["bottom"]
            layout_list.append(left)
            layout_list.append(top)
            layout_list.append(right)
            layout_list.append(bottom)
            return layout_list

    # def takeScreen_Part(self, image_name, **keyargs):
    #     imagepath = "/sdcard/1.png"
    #     if self.sn == None:
    #         subprocess.Popen("adb shell rm " + imagepath).wait()
    #         subprocess.Popen("adb shell screencap -p " + imagepath).wait()
    #         subprocess.Popen("adb pull " + imagepath + " " + rootPath + "\\resource\image\\" + image_name + ".png").wait()
    #         subprocess.Popen("adb shell rm " + imagepath).wait()
    #     else:
    #         subprocess.Popen("adb -s %s shell rm " % self.sn + imagepath).wait()
    #         subprocess.Popen("adb -s %s shell screencap -p " % self.sn + imagepath).wait()
    #         subprocess.Popen("adb -s %s pull " % self.sn + imagepath + " " + rootPath + "\\resource\image\\" + image_name + ".png")
    #         os.popen("adb -s %s shell rm " % self.sn + imagepath).wait()
    #         subprocess.Popen("adb -s %s shell rm " % self.sn + imagepath).wait()
    #
    #     layout_list = self.getLayout(**keyargs)
    #     im = Image.open(rootPath + "\\resource\image\\" + image_name + ".png")
    #     im = im.crop((layout_list[0], layout_list[1], layout_list[2], layout_list[3]))
    #     im.save(rootPath + "\\resource\image\\" + image_name + ".png")

    # def takeScreen_Part_Byxy(self, image_name, left, top, right, bottom):
    #     imagepath = "/sdcard/1.png"
    #     if self.sn == None:
    #         subprocess.Popen("adb shell rm " + imagepath).wait()
    #         subprocess.Popen("adb shell screencap -p " + imagepath).wait()
    #         subprocess.Popen(
    #             "adb pull " + imagepath + " " + rootPath + "\\resource\image\\" + image_name + ".png").wait()
    #         subprocess.Popen("adb shell rm " + imagepath).wait()
    #     else:
    #         subprocess.Popen("adb -s %s shell rm " % self.sn + imagepath).wait()
    #         subprocess.Popen("adb -s %s shell screencap -p " % self.sn + imagepath).wait()
    #         subprocess.Popen(
    #             "adb -s %s pull " % self.sn + imagepath + " " + rootPath + "\\resource\image\\" + image_name + ".png")
    #         os.popen("adb -s %s shell rm " % self.sn + imagepath).wait()
    #         subprocess.Popen("adb -s %s shell rm " % self.sn + imagepath).wait()
    #
    #     self.wait(2)
    #     im = Image.open(rootPath + "\\resource\image\\" + image_name + ".png")
    #     im = im.crop((left, top, right, bottom))
    #     im.save(rootPath + "\\resource\image\\" + image_name + ".png")

    # def saveRecodingSound(self, audio_time):
    #     '''
    #     record audio
    #     install pyaudio : python -m pip install pyaudio
    #     :param audio_time:recoding time(seconds) ,type:int
    #     :return:
    #     '''
    #     # open the input of wave
    #     with open(rootPath + '\\project.log', 'r') as f:
    #         savePath = f.readline().strip()
    #     casename = inspect.stack()[1][1].split("\\")[-1].split(".py")[0]
    #     if os.path.exists(os.path.join(savePath,casename)):
    #         pass
    #     else:
    #         os.mkdir(os.path.join(savePath,casename))
    #     toolsPath = os.path.join(rootPath, "tools")
    #     config_demo_path = os.path.join(toolsPath, "config_demo.txt")
    #     config_name = "config.txt"
    #     if os.path.exists(os.path.join(toolsPath, config_name)):
    #         os.remove(os.path.join(toolsPath, config_name))
    #     Time = time.strftime('%Y%m%d%H%M%S')
    #     content = open(config_demo_path).read()
    #     with open(os.path.join(toolsPath, config_name), "w") as f:
    #         f.write(content % (os.path.join(savePath,casename), casename+Time))
    #
    #     pa = PyAudio()
    #     stream = pa.open(format=paInt16, channels=CHANNELS,
    #                      rate=RATE, input=True,
    #                      frames_per_buffer=CHUNK)#一个buffer存CHUNK个字节,作为一帧
    #     save_buffer = []
    #     count = 0
    #     for i in range(0, int(RATE / CHUNK * audio_time)):
    #         # read CHUNK sampling data
    #         string_audio_data = stream.read(CHUNK)
    #         save_buffer.append(string_audio_data)
    #         count += 1
    #
    #     stream.stop_stream()
    #     stream.close()
    #
    #     self.save_wave_file(os.path.join(savePath,casename), casename+Time+".wav",save_buffer)
    #     save_buffer = []

    def save_wave_file(self, filepath, filename, data):
        '''''save the date to the wav file'''
        wf = wave.open(os.path.join(filepath,filename), 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(SAMPWIDTH)
        wf.setframerate(RATE)
        wf.writeframes(b"".join(data))
        wf.close()

    def verifyRecordingFile(self):
        '''
        :func 校验录音文件中是否有断续/忽高忽低/杂音等问题
        :return:
        '''
        batPath = os.path.join(rootPath,"tools","startup.bat")
        # print(batPath)
        subprocess.Popen(batPath).wait()

    def killProcessByPid(self, pid):
        """
        :func 通过pid号杀掉程序进程
        :param pid: 进程号
        :return:
        """
        subprocess.Popen("taskkill /F /T /PID %s" % pid)

    def sendSetCliConmand(self, conmand,times=1):
        """
        :func 通过发送指令模拟touch板操作
        :param conmand:  button l/r/u/d/ms/ml 左/右/上/下/短按鸟标/长按鸟标
        :param conmand:  clf c 清除串口标志
        :param times:  点击touch次数，默认点击1次
        :return:
        """
        toolsPath = os.path.join(rootPath, "tools")
        cli_ttl_demo_path = os.path.join(toolsPath, "setCli_demo.ttl")
        setCli_name = "setCli.ttl"
        setCli_bat_name = "setCli.bat"
        if os.path.exists(os.path.join(toolsPath, setCli_name)):
            os.remove(os.path.join(toolsPath, setCli_name))
        content = open(cli_ttl_demo_path).read()
        with open(os.path.join(toolsPath, setCli_name), "w") as f:
            f.write(content % conmand)
        for i in range(times):
            proc = subprocess.Popen(os.path.join(toolsPath, setCli_bat_name))
            self.wait(1)
            pid = proc.pid
            self.killProcessByPid(pid)
            self.wait(0.5)

    def sendGetCliConmand(self, conmand):
        """
        :func 通过发送指令获取touch板状态值
        :param conmand:  p/v/b/d等等,详细信息请看参数文档
        :return:
        """
        toolsPath = os.path.join(rootPath, "tools")
        cli_ttl_demo_path = os.path.join(toolsPath, "getCli_demo.ttl")
        getCli_name = "getCli.ttl"
        getCli_bat_name = "getCli.bat"
        getCli_info_name = "getCli.txt"
        if os.path.exists(os.path.join(toolsPath, getCli_name)):
            os.remove(os.path.join(toolsPath, getCli_name))
        if os.path.exists(os.path.join(toolsPath, getCli_info_name)):
            os.remove(os.path.join(toolsPath, getCli_info_name))
        content = open(cli_ttl_demo_path).read()
        with open(os.path.join(toolsPath, getCli_name), "w") as f:
            f.write(content % (toolsPath, getCli_info_name, conmand))
        proc = subprocess.Popen(os.path.join(toolsPath, getCli_bat_name))
        self.wait(2)
        pid = proc.pid
        self.killProcessByPid(pid)

    def getCliConmandResult(self, conmand, keyword):
        """
        :func 读取get指令后的返回值,并根据命令和关键字识别出具体返回值,必须在sendGetCliConmand方法后面使用
        :param conmand: get指令参数,例如p/v/s/a/m等
        :param keyword: 期望返回值中的关键字,详细数据看cli指令excel表
        :return:
        """
        toolsPath = os.path.join(rootPath, "tools")
        getCli_info_namse = "getCli.txt"
        content = open(os.path.join(toolsPath, getCli_info_namse)).read()
        # print(content)
        if content != "":
            if conmand == "b":
                content = content.split()
                # print(content)  # 例：['Log', 'start', 'get', 'b', 't:72,', 'd:77,', 'lr:46', 'mfb:52', 'c:0', '>']
                if keyword == "t":
                    for _ in content:
                        if "t:" in _:
                            value = _[len("t:"):].strip(",")
                            # print(value)
                            Logger.info("The setgroup lights value is %s"%value)
                            return value
                if keyword == "d":
                    for _ in content:
                        if "d:" in _:
                            value = _[len("d:"):].strip(",")
                            # print(value)
                            Logger.info("The favorite lights value is %s" % value)
                            return value
                if keyword == "lr":
                    for _ in content:
                        if "lr:" in _:
                            value = _[len("lr:"):].strip(",")
                            # print(value)
                            Logger.info("The next/prev lights value is %s" % value)
                            return value
                if keyword == "mfb":
                    for _ in content:
                        if "mfb:" in _:
                            value = _[len("mfb:"):].strip(",")
                            # print(value)
                            Logger.info("The bird logo lights value is %s" % value)
                            return value
                if keyword == "c":
                    for _ in content:
                        if "c:" in _:
                            value = _[len("c:"):].strip(",")
                            # print(value)
                            Logger.info("The volume lights value is %s" % value)
                            return value
                else:
                    raise ValueError("keyword <%s> is an invalid parameter"%keyword)

            if conmand == "p":
                content = content.split("\n")
                # print(content)  # 例：['Log start', 'get p', 'bat level percent = 100 ', 'bat average value = 2630 ', 'bat led level = 10 ', 'bat_recycle = 53 ', 'bat_fcc = 2400 ', 'bat_power_used = 38 ', 'get_charge_state = CHARGED', '> ']
                if keyword == "bat level percent":
                    for _ in content:
                        if "bat level percent" in _:
                            value = _[len("bat level percent = "):].strip()
                            # print(value)
                            Logger.info("The power level percent value is %s" % value)
                            return value
                if keyword == "get_charge_state":
                    for _ in content:
                        if "get_charge_state" in _:
                            value = _[len("get_charge_state = "):].strip()
                            # print(value)
                            Logger.info("The product charge state value is %s" % value)
                            return value
                else:
                    raise ValueError("keyword <%s> is an invalid parameter"%keyword)

            if conmand == "v":
                content = content.split("\n")
                # print(content)  # 例：['Log start', 'get v', 'MCU version: ZippMini_M0.3.172 ', 'bt version: ZippMini_B0.5.34 ', 'dsp version: ZippMini_D0.1.35', 'touch version:\tZippMini_T0.1.527.1', '> ']
                if keyword == "MCU version":
                    for _ in content:
                        if "MCU version" in _:
                            value = _[len("MCU version:"):].strip()
                            # print(value)
                            Logger.info("The mcu version value is %s" % value)
                            return value
                if keyword == "bt version":
                    for _ in content:
                        if "bt version" in _:
                            value = _[len("bt version:"):].strip()
                            # print(value)
                            Logger.info("The bt version value is %s" % value)
                            return value
                if keyword == "dsp version":
                    for _ in content:
                        if "dsp version" in _:
                            value = _[len("dsp version:"):].strip()
                            # print(value)
                            Logger.info("The dsp version value is %s" % value)
                            return value
                if keyword == "touch version":
                    for _ in content:
                        if "touch version" in _:
                            value = _[len("touch version:"):].strip()
                            # print(value)
                            Logger.info("The touch version value is %s" % value)
                            return value
                else:
                    raise ValueError("keyword <%s> is an invalid parameter"%keyword)

            if conmand == "d":
                content = content.split("\n")
                # print(content)  # 例：['Log start', 'get d', 'favor ch state:1 1 1 1 1 ', 'favor_choosed:0', '> ']
                if keyword == "favor ch state":
                    for _ in content:
                        if "favor ch state" in _:
                            value = _[len("favor ch state:"):].strip()
                            # print(value)
                            Logger.info("The favor ch state value is %s" % value)
                            return value
                if keyword == "favor_choosed":
                    for _ in content:
                        if "favor_choosed" in _:
                            value = _[len("favor_choosed:"):].strip()
                            # print(value)
                            Logger.info("The current favor_choosed value is %s" % value)
                            return value

        else:
            raise ValueError("The file named %s is null"%getCli_info_namse)

    def setFavoriteChannel(self,channel = "0",timeout=30):
        '''
        :func 通过点击touch板中心形灯切换喜爱频道
        :param channel: 期望切换的频道，默认是0频道
        :param timeout: 切换频道超时时间
        :return:
        '''
        self.sendSetCliConmand("button d")
        startTime = time.time()
        while time.time() - startTime < timeout:
            self.sendGetCliConmand("d")
            if self.getCliConmandResult("d","favor_choosed") == channel:
                Logger.info("current favor_channel is %s"%channel)
                break
            else:
                self.wait(3)
                self.sendSetCliConmand("button d",times=2)

    def getConfigForAudio(self):
        with open(rootPath + '\\project.log', 'r') as f:
            savePath = f.readline().strip()
            # print(savePath)
        casename = inspect.stack()[1][1].split("/")[-1].split(".py")[0]
        # print(casename)
        if os.path.exists(os.path.join(savePath,casename)):
            pass
        else:
            os.mkdir(os.path.join(savePath,casename))
        toolsPath = os.path.join(rootPath, "tools")
        config_demo_path = os.path.join(toolsPath, "config_demo.txt")
        config_name = "config.txt"
        if os.path.exists(os.path.join(toolsPath, config_name)):
            os.remove(os.path.join(toolsPath, config_name))
        content = open(config_demo_path).read()
        with open(os.path.join(toolsPath, config_name), "w") as f:
            f.write(content % (os.path.join(savePath,casename), casename+".wav"))

    def get_imei(self):
        # return os.system("adb shell getprop gsm.imei.sub0")   只du取
        B=os.popen("adb shell getprop gsm.imei.sub0","r").read().strip() #du取並可用
        return B

    def get_version(self):
        # return os.system("adb shell getprop gsm.imei.sub0")
        C=os.popen("adb shell getprop ro.product.version.software","r").read().strip()
        return C






if __name__ == "__main__":
    A=Common().get_imei()
    print(A)
    D=Common().get_version()
    print(D)

    # Common().sound_Record(10)
        # Common().sound_Record()
        # Common().sendSetCliConmand("button d")
        # Common().sendGetCliConmand("d")
        # Common().setFavoriteChannel()
        # Common().getCliConmandResult("v", "touch version")
        # for i in range(100):
        #     Common().sendSetCliConmand("button u")
        #     Common().sendSetCliConmand("button ms")
        #     Common().sendSetCliConmand("button r")
        #     Common().sendSetCliConmand("button u")
        #     Common().sendSetCliConmand("button l")
        #     Common().wait(3)
    # audio_path = os.path.join(rootPath, 'report') + '\\'
    # audio_name = time.strftime("%Y-%m-%d_%H-%M-%S") + '.wav'
    # Common().setPowerOnWhenOff(port="COM15",timeout=5,disc=20)
    # Common().getLedBrightnessValue(port=CONST.SERIALNUMBER.COM15,timeout=3)

