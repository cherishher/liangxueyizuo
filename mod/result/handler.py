# -*- coding: utf-8 -*-
# @Date    : 2016/5/22  16:57
# @Author  : 490949611@qq.com
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import update

from mod.db.member import Member
import tornado.web
from ..db.questions import Questions
from ..db.user_answer import Answer
from ..db.answer_cache import Answer_cache
from config import *
import datetime
import json,urllib
import traceback

class ResultHandler(tornado.web.RequestHandler):

	@property
	def db(self):
		return self.application.db

	def on_finish(self):
		self.db.close()

	def get_current_user(self):
		return self.get_secure_cookie("user")

	def get(self):
		if not self.current_user:
			self.redirect("/login")
			return
		else:
			#成绩界面
			try:
				userid = self.get_argument("userid")
				goal = self.get_argument("goal")
				if not (userid or goal):
					self.write("params lack!")
				data = {
					'userid':userid,
					'goal':goal
				}
				self.render("succeed.html",data = data)
			except Exception,e:
				print str(e)

	def post(self):
		# if not self.current_user:
		# 	self.redirect("/login")
		# 	return
		# else:
			#获取时间
			usertime = self.get_argument("time")
			if usertime:
				print "usertime:",usertime
			else:
				print "no data comes"

			#获取答案
			data = self.db.query(Questions).all()
			question_num = 10
			count = 0
			correct_answer=[]
			answer_data = self.db.query(Answer_cache.answer).filter(Answer_cache.studentnum == self.current_user).one()
			user_answerCache = []
			user_answer=''
			for i in range(1,11):
					temp2 = answer_data.answer.split('{')[i].split('}')[0].split('"')[3]
					correct_answer.append(temp2)
			try:
				for i in range(0,question_num):
					temp = self.get_argument("question"+str(i),default='blank')
					print temp
					user_answerCache.append(temp)
					if temp == correct_answer[i]:
						count += 10
			except Exception,e:
				traceback.print_exc()
				self.write(u"失败了。。。似乎发生了什么奇怪的事情呢！")

			#保存成绩
			for i in range(0,len(user_answerCache)):
				user_answer += user_answerCache[i]+' '
			try:
				answer = self.db.query(Answer).filter(Answer.username == self.current_user).one()
				restchance = answer.chance
				if restchance < 0:
					self.redirect("/result")
					return
				else:
					answer.answer = user_answer
					if answer.goal < count:
						try:
							answer.time = usertime
							answer.goal = count
							answer.chance = restchance-1
							self.db.commit()
						except Exception,e:
							print str(e)
					else:
						try:
							answer.chance = restchance-1
							self.db.commit()
						except Exception,e:
							print str(e)
			except NoResultFound:
				try:
					user_answer = Answer(username = self.current_user,goal = count,degree = DEGREE,answer = user_answer,time = usertime)
					self.db.add(user_answer)
					self.db.commit()
				except Exception,e:
					print str(e)
					self.write(u"提交失败了T_T,重新提交一次呗")

			except Exception,e:
				print str(e)



			#成绩界面
			data = {
				'userid':self.current_user,
				'goal':count
			}
			self.write(json.dumps(data))



