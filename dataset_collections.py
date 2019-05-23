# coding: utf-8
import random
import sys
import urllib.request
import re

import chardet
import jieba

full_text = ""   # 所有章节内容
# full_text = open("data/douluo_chapters.txt", "r", encoding='utf-8').read()
full_lines = []  # 结果的每一行


# 获取网页源码
def get_html(url):
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    req = urllib.request.Request(url=url, headers=headers)
    html = urllib.request.urlopen(req)
    return html.read().decode('utf-8', 'ignore')


# 保存到文本文件
def save_text_file(file_name, contents):
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(contents)


def get_tangsan_chapters(begin_page, end_page, name):
    global full_text
    chapters_text = ""
    for page in range(begin_page, end_page+1):
        html = get_html("http://www.tangsanshu.com/douluodalu/"+str(page)+".html")
        contents = re.findall(
            '<div id="content" class="showtxt">((?:.|\n)+?)(?:</div>|http)'
            , html)
        # print(contents)
        if len(contents) != 0:
            content = str(contents[0])
            # 处理下载的文本
            content = content.replace("&nbsp;", "").replace("<br />", "").replace("\n\n", "\n").replace("　", "").replace(" ", "")
            chapters_text += content + "\n"
            print(name, "(", str(page-begin_page+1), " / ", str(end_page-begin_page+1), ") : ", len(content))
    save_text_file("data/"+name+".txt", chapters_text)
    full_text += chapters_text


# 处理所有文本
def process_chapters(chapters):
    paras = chapters.split("\n")
    index = 0
    size = len(paras)
    for para in paras:
        print("process ", str(index), "/", str(size), ":", para)
        index = index + 1
        process_lines(para)
    save_text_file("data/tangsan_dataset.txt", "\n".join(full_lines))


# 处理每一段落
def process_lines(para):
    global full_lines
    if para.strip() == '':
        return
    pos = 0
    it = re.finditer(r"[。？！]", para)
    for p in it:
        fp = p.start()
        sent = para[pos:fp]
        punc = para[fp:fp+1]
        # print(sent, "-->", para[fp:fp+1])
        pos = fp+1
        full_lines += ["__label__" + punc + " " + " ".join(jieba.cut(sent))]


# =========================================================================
# 斗罗大陆 http://www.tangsanshu.com/douluodalu/2253.html


if full_text == "":
    get_tangsan_chapters(2253, 2855, "斗罗大陆")  # 斗罗1
    get_tangsan_chapters(3556, 5433, "绝世唐门")  # 斗罗2
    get_tangsan_chapters(5435, 17128, "龙王传说")  # 斗罗3
    save_text_file("data/tangsan_chapters.txt", full_text)

process_chapters(full_text)
