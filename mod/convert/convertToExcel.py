# -*- coding: utf-8 -*-
# @Date    : 2016/6/26  20:44
# @Author  : 490949611@qq.com
import re


def readTxt():
	f = open("G:/ThingsOfMax/project/liangxueyizuo/materia/question.txt",mode='r')
	while True:
		line = f.readline()
		if re.match(r'\w、',line):
			print(line)


if __name__ == '__main__':
    readTxt()
