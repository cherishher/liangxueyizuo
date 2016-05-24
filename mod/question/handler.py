# -*- coding: utf-8 -*-
# @Date    : 2016/5/22  16:57
# @Author  : 490949611@qq.com
from mod.db.member import Member
import tornado.web
from ..db.questions import Questions
import datetime
import random
import json,urllib
from tornado.httpclient import HTTPRequest,HTTPClient

class QuestionHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

	def on_finish(self):
		self.db.close()

	def swap(self,a,b):
		c = a
		a = b
		b = c

	def get(self):
		data = self.db.query(Questions).all()
		question_num = len(data)
		#数据要处理成随机的！
		mydata = []
		rand = []
		for i in range(question_num):
			rand.append(i)
		for i in range(question_num):
			temp1 = random.randint(0,question_num-1)
			temp2 = random.randint(0,question_num-1)
			c = rand[temp1]
			rand[temp1] = rand[temp2]
			rand[temp2] = c

		for i in range(question_num):
			mydata.append(data[rand[i]])
		# for item in data:
		# 	print item.id
		# print mydata
		self.render('questions.html',data = mydata)

	def post(self):
		data = self.db.query(Questions).all()
		question_num = len(data)
		count = 0
		user_answer={}
		for i in range(1,question_num+1):
			temp = self.get_argument(str(i),default=None)
			print temp
