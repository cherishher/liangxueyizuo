# -*- coding: utf-8 -*-
# @Date    : 2016/5/22  16:57
# @Author  : 490949611@qq.com
from mod.db.member import Member

import tornado.web
import Cookie
from sqlalchemy.orm.exc import NoResultFound
from ..db.questions import Questions
from ..db.user_answer import Answer
from ..db.answer_cache import Answer_cache
from config import *
import datetime
import random

4+6
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
			flag = True
			restchance = 3
			retjson = {
				'content':u''
			}
			try:
				answer = self.db.query(Answer).filter(Answer.username == self.current_user).one()
				restchance = answer.chance
				if restchance <= 0:
					self.redirect("/result")
					return
				else:
					self.showquestion()
			except NoResultFound:
				self.showquestion()


	def showquestion(self):
				data = self.db.query(Questions).all()
				first = 0
				question_num = len(data)
				#数据要处理成随机的！
				mydata = []
				myanswer = []
				self.random1 = self.get_random(first,question_num)
				for i in range(0,10):
					temp = {
						'id':i,
						'question':data[self.random1[i]].question,
						'answer1':data[self.random1[i]].answer1,
						'answer2':data[self.random1[i]].answer2,
						'answer3':data[self.random1[i]].answer3,
						'answer4':data[self.random1[i]].answer4
					}
					mydata.append(temp)
					myanswer.append(data[self.random1[i]].answer)
				sqlanswer = json.dumps(myanswer)
				try:
					result = self.db.query(Answer_cache).filter(Answer_cache.studentnum==self.current_user).one()
					result.answer = sqlanswer
				except NoResultFound:
					cache = Answer_cache(studentnum=self.current_user,answer=sqlanswer)
					self.db.add(cache)
				self.db.commit()
				self.render('questions.html',data = mydata)

	def post(self):
		retjson = {
			'code':200,
			'text':u'欢迎参与答题。本次答题限时30分钟，每人共有三次答题机会，计时开始'
		}
		# start_time = self.get_argument('start_time',default=0)
		now_time = self.get_argument('now_time',default=0)
		print 'now_time',now_time
		if now_time:
			if int(now_time) == 25:
				retjson['code'] = 300
				retjson['text'] = u'剩余答题时间只有5分钟，请尽快答题'
			if int(now_time) >= 30:
				retjson['code'] = 400
				retjson['text'] = u'答题时间结束，将自动提交当前答案'
		self.write(json.dumps(retjson))
		# time = self.get_argument('time')#向数据库保存当前时间
		# totaltime = 0
		# if time:
		# 	totaltime += time
		# user_answer = Answer(username = self.current_user,goal = 0,time = 0,type = ANSWER_TYPE)
		# self.db.add(user_answer)
		# self.db.commit()#数据库操作

