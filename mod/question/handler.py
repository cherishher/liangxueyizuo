# -*- coding: utf-8 -*-
# @Date    : 2016/5/22  16:57
# @Author  : 490949611@qq.com
from mod.db.member import Member
import tornado.web
import Cookie
from ..db.questions import Questions
import datetime
import random
import json,urllib
from tornado.httpclient import HTTPRequest,HTTPClient

class QuestionHandler(tornado.web.RequestHandler):
	random=[]

	@property
	def db(self):
		return self.application.db

	def get_current_user(self):
		return self.get_secure_cookie("user")

	def on_finish(self):
		self.db.close()

	def get_random(self,first,len):
			rand = []
			for i in range(first,len):
				rand.append(i)
			for i in range(first,len):
				temp1 = random.randint(first,len-1)
				temp2 = random.randint(first,len-1)
				c = rand[temp1]
				rand[temp1] = rand[temp2]
				rand[temp2] = c
			return rand


	def get(self):
		if not self.current_user:
			self.redirect("/login")
			return
		else:
			data1 = self.db.query(Questions).filter(Questions.type == 1).all()
			data2 = self.db.query(Questions).filter(Questions.type == 2).all()
			data3 = self.db.query(Questions).filter(Questions.type == 3).all()
			question_num = len(data1)
			first = 0
			#数据要处理成随机的！
			mydata = []
			self.random = self.get_random(first,question_num)
			for i in range(question_num):
				mydata.append(data1[self.random[i]])
			for i in range(question_num):
				mydata.append(data2[self.random[i]])
			for i in range(question_num):
				mydata.append(data3[self.random[i]])
			# for item in data:
			# 	print item.id
			# print mydata
			self.render('questions.html',data = mydata)

