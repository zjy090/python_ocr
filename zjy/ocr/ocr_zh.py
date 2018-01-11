# -*- coding: utf-8 -*-

import os
import pytesseract
from PIL import Image
import screenshot
import time
import webbrowser
import urllib
import numpy as np
import cv2
from sklearn.svm import SVC
from sklearn.externals import joblib

import subprocess
import os
import sys
from PIL import Image



def main():
    """
    主函数
    """
    op = yes_or_no('请确保手机打开了 ADB 并连接了电脑，'
                   '然后打开头脑王者后再用本程序，确定开始？')
    if not op:
        print('bye')
        return
    #核心递归
    ocr_subject_parent()

    # for root, sub_dirs, files in os.walk('E:/临时接收的文件/知乎答题/百万/'):
    #     for file in files:
    #         print('发现图片:' + file)
    #         img = Image.open('E:/临时接收的文件/知乎答题/百万/'+file)
    #         ocr_subject(img)


def yes_or_no(prompt, true_value='y', false_value='n', default=True):
    """
    检查是否已经为启动程序做好了准备
    """
    default_value = true_value if default else false_value
    prompt = '{} {}/{} [{}]: '.format(prompt, true_value,
                                      false_value, default_value)
    i = input(prompt)
    if not i:
        return default
    while True:
        if i == true_value:
            return True
        elif i == false_value:
            return False
        prompt = 'Please input {} or {}: '.format(true_value, false_value)
        i = input(prompt)


def screenImg(true_value='', default=True):
    prompt = '当出现题目时，请按下回车进行识别 '
    i = input(prompt)
    if not i:
        return default
    while True:
        if i == true_value:
            return True
        else:
            return False
        i = input(prompt)


def ocr_subject(p):
    # 截取 距离上530开始  940结束
    # 截取 距离上260  570结束
    p = cut_img(p)
    pytesseract.pytesseract.tesseract_cmd = 'E:/Program Files (x86)/Tesseract-OCR/tesseract'
    subject = pytesseract.image_to_string(p, lang='chi_sim')
    subject = "".join(subject.split())
    # subject = subject.split('.')[1]
    print(subject)
    openPage(subject)
    ocr_subject_parent()


def ocr_subject_parent():
    result = screenImg()
    if result:
        start = time.time()
        # screenshot.check_screenshot()
        process = subprocess.Popen(
            'adb shell screencap -p',
            shell=True, stdout=subprocess.PIPE)
        binary_screenshot = process.stdout.read()
        binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
        f = open('autojump.png', 'wb')
        f.write(binary_screenshot)
        f.close()
        # screenshot.pull_screenshot()
        img = Image.open('autojump.png')
        ocr_subject(img)
        print("耗时:" + str(time.time() - start))



def openPage(subject):
    url = 'https://www.baidu.com/s?wd={}'.format(
        subject)
    webbrowser.open(url)
    webbrowser.get()



def cut_img(img):
    region = img.crop((0, 570, 1080, 920))
    #region.save("temp/cut_first.png")
    return region


if __name__ == '__main__':
    main()
