# -*- coding: utf-8 -*-
# @Date    : 2016/5/22  16:57
# @Author  : 490949611@qq.com
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import update

from mod.db.member import Member
from ..db.questions import Questions
import tornado.web
from ..db.answer_cache import Answer_cache
from ..db.user_answer import Answer
import traceback
import json

class ReviewHandler(tornado.web.RequestHandler):

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

			#取之前随机生成的答案
			try:
				data = self.db.query(Answer_cache).filter(Answer_cache.studentnum == self.current_user).one()
				temp = []
				user_temp = []
				mydata = []
				for i in range(1,11):
					temp2 = data.answer.split('{')[i].split('}')[0].split(':')[2]
					temp.append(int(temp2))
			#取用户填写的答案
				answer = self.db.query(Answer).filter(Answer.username == self.get_current_user()).one()
				for i in range(0,10):
					temp1 = answer.answer.split(' ')[i]
					user_temp.append(temp1)
			#比较逻辑
				for i in range(0,len(temp)):
					question = self.db.query(Questions).filter( Questions.id == temp[i]).one()
					rightAnswer = question.answer
					state = 1
					if user_temp[i] != rightAnswer:
						state = 0
					else:
						pass
					newquestion = {
						'id':i,
						'question':question.question,
						'answer1':question.answer1,
						'answer2':question.answer2,
						'answer3':question.answer3,
						'answer4':question.answer4,
						'answer': rightAnswer,
						'state': state
					}
					mydata.append(newquestion)
				self.render("questionsdetail.html",data = mydata)
			except NoResultFound:
				self.write("<H1>page not found, sorry!</H1>")
			except Exception,e:
				traceback.print_exc()
				self.write("<H1>server error,sorry!</H1>")





