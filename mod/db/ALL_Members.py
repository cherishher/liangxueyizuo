# -*- coding: utf-8 -*-
# @Date    : 2016/6/8  14:24
# @Author  : 490949611@qq.com
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import engine

Base = declarative_base()

class AllMembers(Base):
	__tablename__ = 'xjexp'
	studentnum = Column(String(64), primary_key=True)
	name = Column(String(64), nullable=False)
	PYCC = Column(String(4096),nullable=False)
	college = Column(String(4096),nullable=False)
	YKTH = Column(String(64), nullable=False)


if __name__ == '__main__':
	Base.metadata.create_all(engine)