# -*- coding: utf-8 -*-

from flask import Flask
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

app = Flask(__name__)

@app.route('/')
def hello():
    engine = create_engine('sqlite:///log.db', echo=False)
    se = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
    Base = declarative_base()
    Base.query =  se.query_property()

    class Log(Base):
        __tablename__ = 'log'
        no = Column(Integer, primary_key=True)
        log = Column(String)
        def __init__(self, no, log):
            self.no = no
            self.log = log
    class Count(Base):
        __tablename__ = 'count'
        cnt = Column(Integer, primary_key=True)
        def __init__(self, cnt):
            self.cnt = cnt

    how = se.query(Count.cnt).filter(Count.cnt != None).all()
    how = how[0][0]
    for i in range(1,how+1):
        if i == 1:
            log = se.query(Log.log).filter(Log.no == i).all()
            log = log[0][0]
            #print(log)
        else:
            thing = se.query(Log.log).filter(Log.no == i).all()
            #print(thing[0][0])
            log = log + '<br>' +thing[0][0]
    #a = "<h1>a</h>"
    
    return log

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=27570, debug=True)
