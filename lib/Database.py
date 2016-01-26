#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python Version: 2.6 - Platform: RedHat Enterprise Linux 5.10 64bits
# Created by Jonathan LAMBERT - contact@jonathanlambert.info

__author__ = "Jonathan LAMBERT"

import cx_Oracle

class Oracle:

	def __init__(self, user, passwd, instance):
		self.user = user
		self.passwd = passwd
		self.instance = instance
		self.connection = None
		
	def connect(self):
		if self.user.lower() == "sys":
			self.connection = cx_Oracle.connect(user=self.user,password=self.passwd,dsn=self.instance, mode = cx_Oracle.SYSDBA)
		else:
			self.connection = cx_Oracle.connect(user=self.user,password=self.passwd,dsn=self.instance)

	
	def disconnect(self):
		self.connection.close()
		
	def execDdl(self, req):
		cur = self.connection.cursor()
		cur.execute(req)
		self.connection.commit()
		cur.close()
		
	def execSelect(self, req, headers=False):
		returnList=[]
		cur = self.connection.cursor()
		try:
			cur.execute(req)
		except cx_Oracle.DatabaseError as e:
			return ("ERROR", e)
		res = cur.fetchall()
		for r in res:
			returnList.append(r)
		if headers:
			cols=[]
			for col in cur.description:
				cols.append(col[0])
			returnList.insert(0, cols)
		cur.close()
		return returnList
	
	def callProc(self, proc, args):
		cur = self.connection.cursor()
		cur.callproc(proc, args)
		cur.close()

	def connected(self):
		try:
			res=self.execSelect("select 1 from dual")
			if res[0][0] == 1:
				return True
		except:
			return False


