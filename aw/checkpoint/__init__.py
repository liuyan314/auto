# -*- coding:utf-8 -*-
'''
Created on 2017.06

@author: chubaoliang
'''

import time
import json
import os, sys
import unittest
from functools import reduce
from logger import Logger
from uiautomator import Device

# from PIL import Image
# from PIL import ImageDraw
import math
import operator
import subprocess
import inspect

rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))

def config():
    jsonFile = "project.json"
    with open(rootPath + "\\" + jsonFile, "r") as f:
        config = json.load(f)
    return config

def check(func):
    def wrapper(*args, **kwargs):
        flag = func(*args, **kwargs)
        if Checkpoint().logConfig("log") == "on":
            if flag == True and Checkpoint().logConfig("pass") == "off":
                pass
            else:
                None
                # Checkpoint().catchLog()
        return flag

    return wrapper

class checkPointResult(Exception):
    pass

class Checkpoint(object):
    def __init__(self, sn=None):
        global d
        d = Device(sn) #实例化，Device是个类
        self.sn = sn
        self.rootPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
        self.record = time.strftime("%Y-%m-%d_%H-%M-%S")

    def logConfig(self, item):
        jsonFile = "project.json"
        with open(self.rootPath + "\\" + jsonFile, "r") as f:
            DATA = json.load(f)
        config = DATA["log_config"][item]
        return config

    def catchLog(self):
        with open(self.rootPath + "\\project.log", "r") as f:
            savePath = f.readline().strip()
        if self.logConfig("log") == "on":
            logPath = savePath + "\\log_" + self.record
            Logger.info("===正在抓取LOG===")
            if not os.path.exists(logPath):
                os.makedirs(logPath)
            sn = self.sn if self.sn != None else "None"
            hwinfo = os.popen("adb -s %s shell getprop ro.hardware" % sn).read() if sn != "None" else os.popen(
                "adb shell getprop ro.hardware").read()
            hwinfo = hwinfo.strip()
            #         print hwinfo
            if "qcom" in hwinfo:
                os.system(self.rootPath + "\\tools\\catchlog_qc.bat " + sn + " " + logPath)
            if "mt" in hwinfo:
                os.system(self.rootPath + "\\tools\\catchlog_mt.bat " + sn + " " + logPath)
            Logger.info("===LOG抓取完成===")
        else:
            pass

    @check
    def checkIfExist(self, message="检测点", timeout=2,**keyargs):
        '''
        1.检查控件是否存在（text， id等）
        '''
        key = list(keyargs.keys())[0]
        value = keyargs[key]
        Logger.info(message + ":")
        startTime = time.time()
        while time.time() - startTime < timeout:
            if not d.exists(**keyargs):
                time.sleep(0.5)
                continue
            else:
                time.sleep(0.5)
                Logger.info("Pass,属性%s " % key + ":" + "\"%s\" 存在于当前页面" % value)
                return True
        else:
            Logger.error("Failed, %s " % key + ":" + "\"%s\" not exist in current window" % value)
            return False

    @check
    def checkIfNotExist(self, message="检测点", timeout=2,**keyargs):
        key = list(keyargs.keys())[0]
        value = keyargs[key]
        Logger.info(message + ":")
        startTime = time.time()
        while time.time() - startTime < timeout:
            if not d.exists(**keyargs):
                Logger.info("Pass,属性%s " % key + ":" + "\"%s\" 不存在于当前页面" % value)
                return True
            else:
                time.sleep(0.5)
                continue
        else:
            Logger.error("Failed, %s " % key + ":" + "\"%s\" not exist in current window" % value)
            return False

    @check
    def checkIfTextExistBySwipe(self, message="", text="", direction="up_down", timeout=10):
        print(message + ":")
        startTime = time.time()
        while time.time() - startTime < timeout:
            if d(text=text).exists:
                Logger.info("text: " + text + " exist in current window")
                time.sleep(1)
                return True
            else:
                if direction == "up_down":
                    d.swipe(500, 800, 500, 200, 50)
                if direction == "left_right":
                    d.swipe(700, 500, 100, 500, 30)
                time.sleep(1.5)
        else:
            Logger.error("text: " + text + " not exist in current window")
            return False

    @check
    def checkTextExistByIdWithFuzzy(self, message="检测点", timeout=5, id=id,text="",fuzzy=True):
        '''
        1.通过模糊匹配方式检查文本是否存在
        '''
        Logger.info(message + ":")
        startTime = time.time()
        if fuzzy:
            while time.time() - startTime < timeout:
                if text in d(resourceId=id).info["text"]:
                    Logger.info("text: " + text + " exist in current window")
                    time.sleep(0.5)
                    return True
                else:
                    time.sleep(0.5)
            else:
                Logger.error("text: " + text + " not exist in current window")
                return False
        else:
            Logger.info("fuzzy is not True")

    def imageSimilarity(self, stdImage, cmpImage):
        '''
        param stdImage: 标准图片
        param cmpImage: 对比图片
        param mode: Phone，手机抓图；Camera，相机抓图
        '''
        image1 = self.rootPath + "\\resource\\image\\" + stdImage
        image2 = self.rootPath + "\\resource\\image\\" + cmpImage

        image1 = Image.open(image1)
        image2 = Image.open(image2)
        h1 = image1.histogram()
        h2 = image2.histogram()
        SV = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        # print(SV)
        return SV

    def _screenShot(self):
        with open(rootPath + '\\project.log', 'r') as f:
            savePath = f.readline().strip()
        if config()['log_config']['screencap'] == 'yes':
            record = time.strftime('%Y-%m-%d_%H-%M-%S')
            imagepath = '/data/local/tmp/' + record + '.png'
            sn = config()['device']['SUBDUT1']['sn']
            if sn == 'None':
                subprocess.Popen('adb shell screencap -p ' + imagepath, shell=True).wait()
                subprocess.Popen('adb pull ' + imagepath + ' ' + savePath + '\\' + record + '.png', shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                print("<a href=\"" + savePath + "\\" + record + ".png\"" + " target=\"_blank\">点击查看截图</a>")
                subprocess.Popen('adb shell rm ' + imagepath).wait()
            else:
                subprocess.Popen('adb -s %s shell screencap -p ' % sn + imagepath, shell=True).wait()
                subprocess.Popen('adb -s %s pull ' % sn + imagepath + ' ' + savePath + '\\' + record + '.png',
                                 shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                print("<a href=\"" + savePath + "\\" + record + ".png\"" + " target=\"_blank\">点击查看截图</a>")
                subprocess.Popen('adb -s %s shell rm ' % sn + imagepath, shell=True).wait()

    @check
    def checkImage(self, stdImage, cmpImage, similar=1):
        '''
        1.图片对比
        param,pls read imageSimilarity
        '''
        _dic = {
            1: 0,
            0.9: 100,
            0.8: 400,
            0.7: 800,
            0.6: 1400,
            0.5: 2000,
            0.1: 5840,
        }

        if self.imageSimilarity(stdImage, cmpImage) > _dic[similar]:
            Logger.error("Fail,图片对比失败")
            return False

        else:
            Logger.info("pass,图片对比成功")
            return True

    ### start ###
    @check
    def checkImageByHist(self, stdImage, cmpImage, similar=1):
        '''
        1.图片对比
        param,pls read imageSimilarity
        '''
        _dic = {
            1: 0,
            0.9: 0.9,
            0.8: 0.8,
            0.7: 0.7,
            0.6: 0.6,
            0.5: 0.5,
            0.1: 0.1,
        }

        if self.calc_similar_by_path(stdImage, cmpImage) > _dic[similar]:
            Logger.info("pass,图片对比成功")
            return True

        else:
            Logger.error("fail,图片对比失败")
            return False

    def make_regalur_image(self,img, size=(256, 256)):
        return img.resize(size).convert("RGB")

    def split_image(self,img, part_size=(64, 64)):
        w, h = img.size
        pw, ph = part_size

        assert w % pw == h % ph == 0

        return [img.crop((i, j, i + pw, j + ph)).copy() \
                for i in range(0, w, pw) \
                for j in range(0, h, ph)]

    def hist_similar(self,lh, rh):
        assert len(lh) == len(rh)
        return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)

    def calc_similar(self,li, ri):
        #	return hist_similar(li.histogram(), ri.histogram())
        return sum(
            self.hist_similar(l.histogram(), r.histogram()) for l, r in
            zip(self.split_image(li), self.split_image(ri))) / 16.0

    def calc_similar_by_path(self, stdImage, cmpImage):
        image1 = self.rootPath + "\\resource\\image\\" + stdImage
        image2 = self.rootPath + "\\resource\\image\\" + cmpImage

        li, ri = self.make_regalur_image(Image.open(image1)), self.make_regalur_image(Image.open(image2))
        # print(self.calc_similar(li, ri))
        return self.calc_similar(li, ri)

    def make_doc_data(self,lf, rf):
        li, ri = self.make_regalur_image(Image.open(lf)), self.make_regalur_image(Image.open(rf))
        li.save(lf + '_regalur.png')
        ri.save(rf + '_regalur.png')
        fd = open('stat.csv', 'w')
        fd.write('\n'.join(l + ',' + r for l, r in zip(map(str, li.histogram()), map(str, ri.histogram()))))
        #	print >>fd, '\n'
        #	fd.write(','.join(map(str, ri.histogram())))
        fd.close()
        li = li.convert('RGB')
        draw = ImageDraw.Draw(li)
        for i in range(0, 256, 64):
            draw.line((0, i, 256, i), fill='#ff0000')
            draw.line((i, 0, i, 256), fill='#ff0000')
        li.save(lf + '_lines.png')

    ### end ###
    @check
    def checkImageNotExists(self, stdImage, cmpImage, similar=1):
        '''
        1.图片对比
        param,pls read imageSimilarity
        '''
        _dic = {
            1: 0,
            0.9: 100,
            0.8: 400,
            0.7: 800,
            0.6: 1400,
            0.5: 2000,
            0.1: 584,
        }

        if self.imageSimilarity(stdImage, cmpImage) > _dic[similar]:
            Logger.info("pass,图片对比成功")
            return True

        else:
            Logger.error("fail,图片对比失败")
            return False

    def checkLedBrightVaule(self, stdValue, cmpValue,disc=10):
        '''
        :func 计算两个值之前的差值，比较是否满足要求
        :param stdValue: 标准值
        :param cmpValue: 对比值，即通过方法获取到的值
        :param disc: 差值，即两个数之前的差值
        :return: 布尔
        '''
        if -abs(disc) <= stdValue - cmpValue <= abs(disc):
            Logger.info("pass,获取值在区间内")
            return True
        else:
            Logger.error("Fail,获取值不在区间内")
            return False

    def checkRecodingSound(self):
        '''
        :func 检测录音文件中生成的txt是否pass
        :return:
        '''
        with open(os.path.join(rootPath,"tools","config.txt"), 'r') as f:
            fileName = f.read().split("\n")[1].replace("wav","txt")
        with open(os.path.join(rootPath, "tools", "config.txt"), 'r') as f:
            filePath = f.read().split("\n")[0]
        with open(os.path.join(filePath, fileName), "r") as f:
            content = f.read().split()
            if "pass" in content :
                Logger.info("Recording sound file comparison result is passed")
                return True
            else:
                Logger.info("Recording sound file comparison result is failed")
                return False