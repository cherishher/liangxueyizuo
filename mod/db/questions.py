# -*- coding: utf-8 -*-
# @Date    : 2016/5/24  19:45
# @Author  : 490949611@qq.com
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import engine


Base = declarative_base()

class Questions(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True)
    question = Column(String(4096), nullable=False)
    answer1 = Column(String(4096),nullable=False)
    answer2 = Column(String(64), nullable=False)
    answer3 = Column(String(4096),nullable=False)
    answer4 = Column(String(4096),nullable=False)
    answer = Column(String(4096),nullable=False)


if __name__ == '__main__':
	Base.metadata.create_all(engine)