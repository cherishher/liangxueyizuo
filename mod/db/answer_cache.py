# -*- coding: utf-8 -*-
# @Date    : 2016/5/30  17:00
# @Author  : 490949611@qq.com
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-3 12:46:36
# @Author  : jerry.liangj@qq.com
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from db import engine


Base = declarative_base()

class Answer_cache(Base):
    __tablename__ = 'answer_cache'
    id = Column(Integer, primary_key=True)
    studentnum = Column(String(64), nullable=False)
    answer = Column(String(4096),nullable=False)


if __name__ == '__main__':
	Base.metadata.create_all(engine)