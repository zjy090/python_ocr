__author__ = 'zjy'
# -*- coding:utf-8 -*-

import pytesseract
import time
import webbrowser
import subprocess
from PIL import Image
import urllib
import urllib.request
import threading
from urllib.parse import quote


def main():
    """
    主函数
    """
    op = yes_or_no('请确保手机打开了 ADB 并连接了电脑，'
                   '然后打开西瓜视频后再用本程序，确定开始？')
    if not op:
        print('bye')
        return
    # 核心递归
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
    prompt = '当出现题目时，请按下回车进行识别 \n'
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
    subImg = cut_img(p)
    pytesseract.pytesseract.tesseract_cmd = 'E:/Program Files (x86)/Tesseract-OCR/tesseract'
    subject = pytesseract.image_to_string(subImg, lang='chi_sim')
    subject = "".join(subject.split())
    subject = subject.split('.')[1].replace("\"", "")
    print(subject)
    ocr_answer(p, subject)
    # openPage(subject)
    # print("结束:" + str(time.time()))
    ocr_subject_parent()


def getSearchNum(key):
    key = quote(key)
    # print(key)
    url = 'http://www.baidu.com/s?wd={}'.format(key)
    # print(url)
    response = urllib.request.urlopen(url)
    page = response.read().decode("utf-8")
    i = int(page.index('百度为您找到相关结果约'))
    start = i + 10
    end = i + 25
    page = page[start: end]
    return page


def ocr_answer(p, subject):
    list = cut_question(p)
    pytesseract.pytesseract.tesseract_cmd = 'E:/Program Files (x86)/Tesseract-OCR/tesseract'
    for p in list:
        t = threading.Thread(target=ocr_answer_thread, args=(p, subject))
        t.start()


def ocr_answer_thread(p, subject):
    answer = pytesseract.image_to_string(p, lang='chi_sim')
    answer = "".join(answer.split())
    v = getSearchNum(subject + ' ' + answer)
    print(answer + ' ' + v)
    # print(time.time())


def ocr_subject_parent():
    result = screenImg()
    if result:
        start = time.time()
        # print("开始:" + str(start))
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


def openPage(subject):
    url = 'https://www.baidu.com/s?wd={}'.format(
        subject)
    webbrowser.open(url)
    webbrowser.get()


def cut_img(img):
    region = img.crop((70, 260, 1025, 570))
    # region.save("temp/cut_first.png")
    return region


def cut_question(img):
    list = []
    question1 = img.crop((70, 590, 1025, 768))
    question2 = img.crop((70, 769, 1025, 947))
    question3 = img.crop((70, 948, 1025, 1130))
    list.append(question1)
    list.append(question2)
    list.append(question3)
    # question1.save("temp/cut_1.png")
    # question2.save("temp/cut_2.png")
    # question3.save("temp/cut_3.png")
    return list


if __name__ == '__main__':
    main()
