#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-3 12:46:36
# @Author  : jerry.liangj@qq.com
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import engine


Base = declarative_base()

class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    studentnum = Column(String(4096), nullable=False)
    password = Column(String(4096),nullable=False)
    name = Column(String(64), nullable=False)
    phonenum = Column(String(4096),nullable=False)
    college = Column(String(4096),nullable=False)
    branch = Column(String(4096),nullable=False)


if __name__ == '__main__':
	Base.metadata.create_all(engine)