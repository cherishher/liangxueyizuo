# -*- coding: utf-8 -*-
# @Date    : 2016/5/22  16:57
# @Author  : 490949611@qq.com

import json

import tornado.web

from mod.db.member import Member
from mod.db.user_answer import Answer

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
			else:
				retjson['code'] = 400
				retjson['text'] = "密码错误，请重新登录"
		except Exception,e:
			print str(e)
			retjson['code'] = 401
			retjson['text'] = "该用户尚未注册，请注册后再登录"
		try:
			print "verify record--"
			answer = self.db.query(Answer).filter(Answer.username == studentnum).one()
			goal = answer.goal
			if answer:
				print "find record"
				retjson['code'] = 300
				retjson['text'] = '亲已经答过题,拿了%d分哦！' % (goal)
		except Exception,e:
			pass
		self.write(json.dumps(retjson))




