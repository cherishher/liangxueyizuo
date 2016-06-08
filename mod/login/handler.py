# -*- coding: utf-8 -*-
# @Date    : 2016/5/22  16:57
# @Author  : 490949611@qq.com

import json
from sqlalchemy.orm.exc import NoResultFound

import tornado.web

from mod.db.member import Member
from mod.db.user_answer import Answer
from config import *

class LoginHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

	def on_finish(self):
		self.db.close()

	def get(self):
		self.render('login.html')

	def post(self):
		#验证用户身份
		retjson={
				'code':200,
				'text':"登录成功,请开始答题"
				}
		flag = True
		studentnum = self.get_argument('studentnum',default=None)
		password = self.get_argument('password',default=None)
		try:
			data = self.db.query(Member).filter(Member.studentnum == studentnum).one()
			if data.password == password:
				self.set_secure_cookie("user",studentnum)
				if studentnum == ADMIN_STUDENTNUM:
					retjson['code'] = 000000
					retjson['text'] = u'欢迎您，管理员！'
			else:
				retjson['code'] = 400
				retjson['text'] = "密码错误，请重新登录"
		except Exception,e:
			print str(e)
			retjson['code'] = 401
			retjson['text'] = "该用户尚未注册，请注册后再登录"
		try:
			answer = self.db.query(Answer).filter(Answer.username == studentnum).one()
			goal = answer.goal
			restchance = answer.chance
			if restchance <= 0:
				retjson['code'] = 300
				retjson['text'] = u'亲答题机会已用完,拿了%d分哦！' % (goal)
			else:
				retjson['code'] = 200
				retjson['text'] = u'还有%d次机会,最高拿了%d分哦！' % (restchance,goal)
		except NoResultFound:
			pass
		self.write(json.dumps(retjson))




