# -*- coding: utf-8 -*-
# @Date    : 2016/6/3  10:31
# @Author  : 490949611@qq.com

import tornado.web

from ..db.material import Material

class StudyHandler(tornado.web.RequestHandler):
	@property
	def db(self):
		return self.application.db

	def on_finish(self):
		self.db.close()

	def get(self):
		material = self.db.query(Material).all()
		self.render('study.html',data = material)