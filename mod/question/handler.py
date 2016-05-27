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
	random1=[]
	random2=[]
	random3=[]

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
			question_num1 = len(data1)
			question_num2 = len(data2)
			question_num3 = len(data3)
			first = 0
			#数据要处理成随机的！
			mydata = []
			self.random1 = self.get_random(first,question_num1)
			self.random2 = self.get_random(first,question_num2)
			self.random3 = self.get_random(first,question_num3)
			for i in range(question_num1):
				mydata.append(data1[self.random1[i]])
			for i in range(question_num2):
				mydata.append(data2[self.random2[i]])
			for i in range(question_num3):
				mydata.append(data3[self.random3[i]])
			# for item in data:
			# 	print item.id
			# print mydata
			self.render('questions.html',data = mydata)

