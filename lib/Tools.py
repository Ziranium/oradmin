#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python Version: 2.6 - Platform: RedHat Enterprise Linux 5.10 64bits
# Created by Jonathan LAMBERT - contact@jonathanlambert.info

__author__ = "Jonathan LAMBERT"

import datetime
import smtplib
import os
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

class Tools:

        def __init__(self):
                self.passFile = '/etc/security/spool/.liste'
                fic=open(self.passFile,"r")
                self.content=fic.read().replace('\t',' ')
                fic.close()

        def getPass(self, dbName, user):
		patterns=[' '+dbName.upper()+'/'+user.lower()+' ', ' '+dbName.upper()+'/'+user.upper()+' ', ' '+dbName.upper()+'/'+user+' ']
		for pattern in patterns:
			if pattern in self.content:
				return self.content.split(pattern)[1].strip().split(' ')[0]
		raise Exception("Les informations d'authentification pour la base "+dbName+" ne sont pas disponible.")

	def getUserDB(self, dbName):
		try:
			userList=[]
			list=self.content.split(' '+dbName.upper()+'/')
			for ind, elem in enumerate(list):
				if ind == 0 or ind == len(list):
					continue
				userList.append(elem.split(' ')[0].strip())
			return userList
		except IndexError, e:
			exitError("Les informations d'authentification pour la base "+dbName+" ne sont pas disponible.")

	def getUserDBCommon(self, dbList):
		dictUserByDB={}
		userListCommon=[]
		for dbName in dbList:
			dictUserByDB[dbName]=self.getUserDB(dbName)
		userListCommon=set(dictUserByDB[dictUserByDB.keys()[0]])
		for dbName, userList in dictUserByDB.iteritems():
			if dbName != dictUserByDB.keys()[0]:
				userListCommon=userListCommon.intersection(userList)
		userListCommon=list(userListCommon)
		return userListCommon
		
	def print_table(self,table):
		aff = ""
		col_width = [max(len(str(x)) for x in col) for col in zip(*table)]
		for line in table:
			aff += "\n| " + " | ".join("{0:{1}}".format(x, col_width[i]) for i, x in enumerate(line)) + " |"
		return aff

	def print_csv(self,table):
		aff=""
		for ligne in table:
			aff += "\n" + ";".join(str(x) for x in ligne)
		return aff

	def timestamp(self):
		now = datetime.datetime.now()
		#return now.strftime("%Y-%m-%d %H:%M:%S")
		return now.strftime("%d-%m-%Y %H:%M:%S")
	
	def sendTextMail(self, exp, dest, sujet, content):
		msg = MIMEText(content)
		msg['Subject'] = sujet
		msg['From'] = exp
		msg['To'] = dest
		s = smtplib.SMTP('localhost')
		s.sendmail(exp, [dest], msg.as_string())
		s.quit()

	def sendMailWithAttachment(self, send_from, send_to, subject, text, files=[], server="localhost"):
		assert type(send_to)==list
		assert type(files)==list
		msg = MIMEMultipart()
		msg['From'] = send_from
		msg['To'] = COMMASPACE.join(send_to)
		msg['Date'] = formatdate(localtime=True)
		msg['Subject'] = subject
		msg.attach( MIMEText(text) )
		for f in files:
			part = MIMEBase('application', "octet-stream")
			part.set_payload( open(f,"rb").read())
			Encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
			msg.attach(part)
		smtp = smtplib.SMTP(server)
		smtp.sendmail(send_from, send_to, msg.as_string())
		smtp.close()


