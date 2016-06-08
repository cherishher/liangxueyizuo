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
				answer = self.db.query(Answer).filter(Answer.username == self.current_user).one()
				data = {
					'userid':answer.username,
					'goal':answer.goal
				}
				self.render("last_succeed.html",data = data)
			except Exception,e:
				print str(e)

	def post(self):
		if not self.current_user:
			self.redirect("/login")
			return
		else:
			data = self.db.query(Questions).all()
			question_num = 10
			count = 0
			correct_answer=[]
			answer_data = self.db.query(Answer_cache.answer).filter(Answer_cache.studentnum == self.current_user).one()
			for item in json.loads(answer_data[0]):
				correct_answer.append(item)
			try:
				for i in range(0,question_num):
					temp = self.get_argument(str(i),default=None)
					if temp == correct_answer[i]:
						count += 10
			except Exception,e:
				print str(e)
				self.write(u"失败了。。。似乎发生了什么奇怪的事情呢！")

			#保存成绩
			try:
				answer = self.db.query(Answer).filter(Answer.username == self.current_user).one()
				restchance = answer.chance
				if restchance < 0:
					self.redirect("/result")
					return
				else:
					if answer.goal < count:
						try:
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
					user_answer = Answer(username = self.current_user,goal = count,degree = DEGREE)
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
			self.render("succeed.html",data = data)




