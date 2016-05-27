# -*- coding: utf-8 -*-
# @Date    : 2016/5/22  16:57
# @Author  : 490949611@qq.com

from mod.db.member import Member
import tornado.web
from ..db.questions import Questions
from ..db.user_answer import Answer
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
			self.render("还是先去做题吧~")


	def post(self):
		if not self.current_user:
			self.redirect("/login")
			return
		else:
			data = self.db.query(Questions).all()
			question_num = len(data)
			count = 0
			user_answer={}
			try:
				for i in range(1,question_num+1):
					temp = self.get_argument(str(i),default=None)
					# qnum = self.random[i-1]
					answer = self.db.query(Questions).filter(Questions.id == i).one()
					print i," ",temp," ",answer.answer
					if temp == answer.answer:
						count += 1
			except Exception,e:
				print str(e)
				self.write(u"失败了。。。似乎发生了什么奇怪的事情呢！")
			#保存成绩
			try:
				user_answer = Answer(username = self.current_user,goal = count)
				self.db.add(user_answer)
				self.db.commit()
			except Exception,e:
				self.write(u"提交失败了T_T,重新提交一次呗")

			#成绩界面
			data = {
				'userid':self.current_user,
				'goal':count
			}
			self.render("succeed.html",data = data)
			self.finish()



