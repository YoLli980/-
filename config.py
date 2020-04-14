import os
DEBUG =True
SECRET_KEY = os.urandom(24)

# 数据库搭建



DIALECT = 'mysql'
# 需要更新链接mysql驱动
# pip install mysql-connector-python mysql-connector-python
#
#
# pip install mysql-connector-python --allow-external mysql-connector-python
#
#
# pip install mysql-connector

DRIVER  = 'mysqlconnector'
USERNAME = 'root'
PASSWORD    = 'nlbq1073'
HOST = '127.0.0.1'
POST = '3306'
DATABASE = 'project_traning'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,POST,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False