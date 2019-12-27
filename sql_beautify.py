#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'SI-GZ-1076'

import re
import os
import sys
# import sqlparse
from tkinter import *
from tkinter.messagebox import askokcancel
from tkinter.filedialog import askopenfilename

def chose_sql():
    """
    返回选择的文件路径及文件名
    """
    file_name = askopenfilename(title='请选择一个要处理的sql文件')
    if file_name == '':
        cancel_flag = askokcancel('提示', '是否想关闭程序？')
        if cancel_flag:
            return ''
        else:
            file_name = chose_sql()
    return file_name

def get_sql_str(file_name):
    """
    读取sql文件，返回一个长字符串
    :param file_name:
    :return:
    """
    with open(file_name, 'r', encoding='utf-8') as f:
        sql_str = f.read()
    return sql_str

def comma_one_space(str):
    """
    如果逗号后面都只有一个空格
    :param str:
    :return:
    """
    return str.replace(',', ', ').replace(',  ', ', ').replace(',  ', ', ')

def load_keywords(sql_dir):
    """
    读取hive关键字，返回一个列表
    :return:
    """
    keywords_file = sql_dir + '\hive_keywords.txt'
    keywords_list = []
    # 添加关键字到列表
    with open(keywords_file, 'r', encoding='utf-8') as f:
        for line in f:
            keywords_list.append(line.strip())
    return keywords_list

def load_functions(sql_dir):
    """
    读取hive函数，返回一个列表
    :return:
    """
    function_file = sql_dir + '\hive_functions.txt'
    function_list = []
    # 添加关键字到列表
    with open(function_file, 'r', encoding='utf-8') as f:
        for line in f:
            function_list.append(line.strip())
    return function_list

def upper_or_lower_keywords(str, flag, sql_dir):
    """
    将输入的sql长字符串中的关键字大写
    :param str:
    :return:
    """
    # 匹配条件，以空字符开头并且空字符（左括号、右括号、逗号）结尾的都匹配出来
    partner = re.compile('(?<=[\s(]).+?(?=[\s(),])', re.S)
    find_words = partner.findall(str)
    keywords = load_keywords(sql_dir)
    for word in find_words:
        if flag == 1:
            # 如果匹配出来的小字符串大写以后是关键词，则将这个小字符串大写
            if word.strip().upper() in keywords:
                p = '(?<=[\s(]){}(?=[\s(),])'.format(word)
                str = re.sub(p, word.upper(), str)
        else:
            # 如果匹配出来的小字符串小写以后是关键词，则将这个小字符串小写
            if word.strip().lower() in keywords:
                p = '(?<=[\s(]){}(?=[\s(),])'.format(word)
                str = re.sub(p, word.lower(), str)
    return str

def upper_or_lower_functions(str, flag, sql_dir):
    """
    将输入的sql长字符串中的函数大写
    :param str:
    :return:
    """
    # 匹配条件，以空字符开头（左括号）并且空字符（左括号、逗号）结尾的都匹配出来
    partner = re.compile('(?<=[\s(=]).+?(?=[\s(,])', re.S)
    find_words = partner.findall(str)
    # print(find_words)
    functions = load_functions(sql_dir)
    for word in find_words:
        if flag == 1:
            # 如果匹配出来的小字符串大写以后是关键词，则将这个小字符串大写
            if word.strip().upper() in functions:
                p = '(?<=[\s(=]){}(?=[\s(,])'.format(word)
                str = re.sub(p, word.upper(), str)
        else:
            # 如果匹配出来的小字符串小写以后是关键词，则将这个小字符串小写
            if word.strip().lower() in functions:
                p = '(?<=[\s(]){}(?=[\s(,])'.format(word)
                str = re.sub(p, word.lower(), str)
    return str

def deal_keywords_functions(str, flag, sql_dir):
    """
    返回关键字和函数都大写的字符串
    :param str:
    :param flag: 1代表大写，2代表小写
    :return:
    """
    if flag in [1, 2]:
        str = upper_or_lower_keywords(str, flag, sql_dir)
        str = upper_or_lower_functions(str, flag, sql_dir)
        return str
    else:
        print('deal_keywords_functions函数第二个入参错误，你应该填写1或者2！')
        return None

def save_deal_sql(str, sql_dir, sql_name):
    """
    保存处理好的sql
    :param sql_dir:
    :return:
    """
    if str is not None:
        save_filename = sql_dir + '\\' + sql_name.split('.')[0] + '_deal' + '.sql'
        with open(save_filename, 'w', encoding='utf-8') as f:
            f.write(str)
        print('sql处理完成！请查看【%s】文件' % os.path.basename(save_filename))

def upper_or_lower_sql(flag):
    """
    入参1代表把关键字和函数处理成大写，2代表处理成小写
    :param flag:
    :return:
    """
    sql_filename = chose_sql()  # 需要处理的sql文件
    sql_dir = os.path.dirname(sql_filename)  # 需要处理的sql文件所在文件夹
    sql_name = os.path.basename(sql_filename)  # 需要处理的sql名

    if sql_filename == '':
        print('你已取消执行程序！')
        return ''
    else:
        sql_str = get_sql_str(sql_filename)  # 读取sql文件
        sql_str = comma_one_space(sql_str)  # 逗号都需要有一个空格
        deal_str = deal_keywords_functions(sql_str, flag, sql_dir)  # 第二个参数1代表大写，2代表小写
        save_deal_sql(deal_str, sql_dir, sql_name)  # 保存处理好对的sql
    return deal_str

# def set_type(str):
#     """
#     调整排版
#     :param str:
#     :return:
#     """
#     partner = re.compile('(?<=[(select)(SELECT)])\s.+?(?=[(from)(FROM)])', re.S)
#     find_strings = partner.findall(str)
#     # print(find_strings[0])
#     # print()
#
#     dict_line = {}
#     # p = re.compile('(?<=\s)[a-z0-9\.]*[a-z0-9_]*,\s*--.+?(?=\s)', re.S)
#     p = re.compile('(?<=\s)[a-z0-9\.]*[a-z0-9_]*,\s*--.+?(?=\s)', re.S)
#     words = p.findall(find_strings[0])
#     print(words)
#     print()
#
#     words_len = len(words)
#     i = 1
#     for word in words:
#         if i == 1:
#             re_word = word.split(',')[0] + '  --' + word.split('-')[-1]
#             str = str.replace(word, re_word)
#         else:
#             re_word = ', ' + word.split(',')[0] + '  --' + word.split('-')[-1] + '\n'
#             str = str.replace(word, re_word)
#         i += 1
#         re_word = ', ' + word.split(',')[0] + '  --' + word.split('-')[-1] + '\n'
#         str = str.replace(word, re_word)
#
#     # for k, v in dict_line.items():
#     #     str = str.replace(k, v)
#
#     str = str.replace('\n\n', '\n')
#     return str


if __name__ == '__main__':

    # str = get_sql_str(r'D:\SheIn\Python\small_tool\sql_beautify\test_sql.sql')
    # str = set_type(str)
    # print(str)

    upper_or_lower_sql(1)  # 命令行的第一个参数（只能为1和2）
    # upper_or_lower_sql(int(sys.argv[1]))  # 命令行的第一个参数（只能为1和2）