#!/usr/bin/python3
# -*- coding:utf-8 -*-
'''
Created on 2019年5月21日
@author: yuejing
'''
import cx_Oracle
from . import fileHandle

def read_sql(file_name) :
	f = open(file_name, "r")
	str = f.read()
	f.close()
	return str

#多维元组转换成多维列表
def lists(tup) :
	b = list(tup)
	for c in b:
		b[b.index(c)] = list(c)
	return b
	
class sqlHandle:

	Config = fileHandle.configyaml('config.yaml').readyaml()

	def __init__(self,host=Config['db_sgm']['host'],db=Config['db_sgm']['server_name'],user=Config['db_sgm']['username'],password=Config['db_sgm']['password']):
		self.host=host
		self.db=db
		self.user=user
		self.password=password

	def sqlTxt(self,path,nStart=0,nNum=-1):
		db_link= self.user+'/'+self.password+'@'+self.host+'/'+self.db
		sql=read_sql(path)
		rt = []
		con = cx_Oracle.connect(db_link)
		cur = con.cursor()    # 获取cursor
		if not cur:
			return rt
		# 查询到列表
		cur.execute(sql)
		if (nStart == 0) and (nNum == 1):
			rt.append(cur.fetchone())
		else:
			rs = cur.fetchall()
			if nNum == - 1:
				rt.extend(rs[nStart:])
			else:
				rt.extend(rs[nStart:nStart + nNum])
		#print("Total: " + str(cur.rowcount)+'行数据')
		con.close()     # 释放cursor
		resul=lists(rt) # 转换成列表
		return resul

	def sqlQuery(self,sql,nStart=0,nNum=-1):
		db_link= self.user+'/'+self.password+'@'+self.host+'/'+self.db
		rt = []
		con = cx_Oracle.connect(db_link)
		cur = con.cursor()    # 获取cursor
		if not cur:
			return rt
		# 查询到列表
		cur.execute(sql)
		if (nStart == 0) and (nNum == 1):
			rt.append(cur.fetchone())
		else:
			rs = cur.fetchall()
			if nNum == - 1:
				rt.extend(rs[nStart:])
			else:
				rt.extend(rs[nStart:nStart + nNum])
		#print("Total: " + str(cur.rowcount)+'行数据')
		con.close()     # 释放cursor
		resul=lists(rt) # 转换成列表
		return resul

