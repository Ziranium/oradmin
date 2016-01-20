#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Jonathan LAMBERT"


import pygtk
pygtk.require('2.0')
import gtk
from Window import Window
import os
import Tools


class Window_statspack(Window):
	def __init__(self, parent, oTool):
		## DATA
		self.oTool = oTool
		self.instanceList = {}
		self.snapList = {}
		self.setInstanceList()
		self.setSnapList()
		## STOCK ITEM
		self.stock_items = (
		("gtk-genSpReport", "", 0, 0, None),
		)
		self.stock_aliases = (
		("gtk-genSpReport", gtk.STOCK_EXECUTE),
		)
		gtk.stock_add(self.stock_items)
		factory = gtk.IconFactory()
		factory.add_default()
		style = gtk.Style()
		for item, alias in self.stock_aliases:
			icon_set = style.lookup_icon_set(alias)
			factory.add(item, icon_set)
		## FENETRE
		self.len_combo_snapYear = 20
		self.len_combo_snapMonth = 20
		self.len_combo_snapDay = 20
		self.len_combo_snapHour = 20
		self.len_combo_snapMinute = 20
		self.len_label_blank = 10
		self.parent=parent
		Window.__init__(self, "Administration Oracle : Statspack")
		self.fenetre.connect("delete_event", self.close_window)
		settings = gtk.settings_get_default()
		settings.props.gtk_button_images = True
		self.vbox_main = gtk.VBox(False, 20)
		self.fenetre.add(self.vbox_main)
		self.frm_res=gtk.Frame("Statspack")
		self.vbox_main.pack_start(self.frm_res, True, True, 0)
		self.vbox_form= gtk.VBox(False, 0)
		self.frm_res.add(self.vbox_form)

		self.frm_instance = gtk.Frame("Instances ")
		self.vbox_instance = gtk.VBox(False, 0)
		self.frm_instance.add(self.vbox_instance)
		
		self.frm_beginTime = gtk.Frame("Begin Time ")
		self.tab_beginTime = gtk.Table(1, 10, False)
		self.frm_beginTime.add(self.tab_beginTime)

		self.frm_endTime = gtk.Frame("End Time ")
		self.tab_endTime = gtk.Table(1, 10, False)
		self.frm_endTime.add(self.tab_endTime)

		self.frm_send = gtk.Frame("Génération ")
		self.vbox_send = gtk.VBox(False, 0)
		self.frm_send.add(self.vbox_send)

		self.entry_mail = gtk.Entry()
		self.entry_mail.set_width_chars(50)
		self.entry_mail.set_text("dest1@sigma.fr;dest2@gmail.com;...")
		self.label_mail = gtk.Label("Adresse(s) mail (obligatoire) : ")
		self.label_mail.set_alignment(xalign=0.0, yalign=0.5)
		self.tab_send = gtk.Table(1, 2, False)
		self.tab_send.attach(self.label_mail, 0, 1, 0, 1)
		self.tab_send.attach(self.entry_mail, 1, 2, 0, 1)

		self.but_generateSpReport=gtk.Button(stock="gtk-genSpReport")
		self.but_generateSpReport.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.but_generateSpReport.connect("clicked", self.generateSpReport)

		self.vbox_send.pack_start(self.tab_send, True, True, 0)
		self.vbox_send.pack_start(self.but_generateSpReport, True, True, 0)

		self.vbox_form.pack_start(self.frm_instance, True, True, 0)
		self.vbox_form.pack_start(self.frm_beginTime, True, True, 0)
		self.vbox_form.pack_start(self.frm_endTime, True, True, 0)
		self.vbox_form.pack_start(self.frm_send, True, True, 0)

		## FORM
		self.setForm()

		self.fenetre.show_all()

	def setForm(self):
		# INSTANCE LIST
		for inst in self.instanceList:
			button = gtk.CheckButton(inst)
			button.connect("toggled", self.setInstChecked, inst)
			self.vbox_instance.pack_start(button, True, True, 0)
		# SNAP LIST
		self.combo_beginSnapYear = gtk.combo_box_new_text()
		self.combo_beginSnapYear.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.combo_beginSnapYear.append_text(" "*self.len_combo_snapYear)
		self.combo_beginSnapYear.connect('changed', self.changeBeginSnapYear)
		self.combo_endSnapYear = gtk.combo_box_new_text()
		self.combo_endSnapYear.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.combo_endSnapYear.append_text(" "*self.len_combo_snapYear)
		self.combo_endSnapYear.connect('changed', self.changeEndSnapYear)

		self.combo_beginSnapMonth = gtk.combo_box_new_text()
		self.combo_beginSnapMonth.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.combo_beginSnapMonth.append_text(" "*self.len_combo_snapMonth)
		self.combo_beginSnapMonth.connect('changed', self.changeBeginSnapMonth)
		self.combo_endSnapMonth = gtk.combo_box_new_text()
		self.combo_endSnapMonth.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.combo_endSnapMonth.append_text(" "*self.len_combo_snapMonth)
		self.combo_endSnapMonth.connect('changed', self.changeEndSnapMonth)

		self.combo_beginSnapDay = gtk.combo_box_new_text()
		self.combo_beginSnapDay.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.combo_beginSnapDay.append_text(" "*self.len_combo_snapDay)
		self.combo_beginSnapDay.connect('changed', self.changeBeginSnapDay)
		self.combo_endSnapDay = gtk.combo_box_new_text()
		self.combo_endSnapDay.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.combo_endSnapDay.append_text(" "*self.len_combo_snapDay)
		self.combo_endSnapDay.connect('changed', self.changeEndSnapDay)

		self.combo_beginSnapHour = gtk.combo_box_new_text()
		self.combo_beginSnapHour.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.combo_beginSnapHour.append_text(" "*self.len_combo_snapHour)
		self.combo_beginSnapHour.connect('changed', self.changeBeginSnapHour)
		self.combo_endSnapHour = gtk.combo_box_new_text()
		self.combo_endSnapHour.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.combo_endSnapHour.append_text(" "*self.len_combo_snapHour)
		self.combo_endSnapHour.connect('changed', self.changeEndSnapHour)
		
		self.combo_beginSnapMinute = gtk.combo_box_new_text()
		self.combo_beginSnapMinute.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.combo_beginSnapMinute.append_text(" "*self.len_combo_snapMinute)
		self.combo_beginSnapMinute.connect('changed', self.changeBeginSnapMinute)
		self.combo_endSnapMinute = gtk.combo_box_new_text()
		self.combo_endSnapMinute.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.combo_endSnapMinute.append_text(" "*self.len_combo_snapMinute)
		self.combo_endSnapMinute.connect('changed', self.changeEndSnapMinute)

		self.label_beginSnapSlash1 = gtk.Label(" / ")
		self.label_beginSnapSlash1.set_alignment(xalign=0.0, yalign=0.5)
		self.label_beginSnapSlash2 = gtk.Label(" / ")
		self.label_beginSnapSlash2.set_alignment(xalign=0.0, yalign=0.5)
		self.label_beginSnapBlank = gtk.Label(" "*self.len_label_blank)
		self.label_beginSnapBlank.set_alignment(xalign=0.0, yalign=0.5)
		self.label_beginSnapDdot = gtk.Label(" : ")
		self.label_beginSnapDdot.set_alignment(xalign=0.0, yalign=0.5)

		self.tab_beginTime.attach(self.combo_beginSnapYear, 0, 1, 0, 1)
		self.tab_beginTime.attach(self.label_beginSnapSlash1, 1, 2, 0, 1)
		self.tab_beginTime.attach(self.combo_beginSnapMonth, 2, 3, 0, 1)
		self.tab_beginTime.attach(self.label_beginSnapSlash2, 3, 4, 0, 1)
		self.tab_beginTime.attach(self.combo_beginSnapDay, 4, 5, 0, 1)
		self.tab_beginTime.attach(self.label_beginSnapBlank, 5, 6, 0, 1)
		self.tab_beginTime.attach(self.combo_beginSnapHour, 6, 7, 0, 1)
		self.tab_beginTime.attach(self.label_beginSnapDdot, 7, 8, 0, 1)
		self.tab_beginTime.attach(self.combo_beginSnapMinute, 8, 9, 0, 1)

		self.label_endSnapSlash1 = gtk.Label(" / ")
		self.label_endSnapSlash1.set_alignment(xalign=0.0, yalign=0.5)
		self.label_endSnapSlash2 = gtk.Label(" / ")
		self.label_endSnapSlash2.set_alignment(xalign=0.0, yalign=0.5)
		self.label_endSnapBlank = gtk.Label(" "*self.len_label_blank)
		self.label_endSnapBlank.set_alignment(xalign=0.0, yalign=0.5)
		self.label_endSnapDdot = gtk.Label(" : ")
		self.label_endSnapDdot.set_alignment(xalign=0.0, yalign=0.5)

		self.tab_endTime.attach(self.combo_endSnapYear, 0, 1, 0, 1)
		self.tab_endTime.attach(self.label_endSnapSlash1, 1, 2, 0, 1)
		self.tab_endTime.attach(self.combo_endSnapMonth, 2, 3, 0, 1)
		self.tab_endTime.attach(self.label_endSnapSlash2, 3, 4, 0, 1)
		self.tab_endTime.attach(self.combo_endSnapDay, 4, 5, 0, 1)
		self.tab_endTime.attach(self.label_endSnapBlank, 5, 6, 0, 1)
		self.tab_endTime.attach(self.combo_endSnapHour, 6, 7, 0, 1)
		self.tab_endTime.attach(self.label_endSnapDdot, 7, 8, 0, 1)
		self.tab_endTime.attach(self.combo_endSnapMinute, 8, 9, 0, 1)
		
		self.setBeginSnapYear()
		self.setEndSnapYear()

		

	def setInstChecked(self, widget, data=None):
		self.instanceList[data]=widget.get_active()

	def setBeginSnapYear(self):
		self.combo_beginSnapYear.get_model().clear()
		self.combo_beginSnapYear.append_text(" "*self.len_combo_snapYear)
		yearList=[]
		for snapId, snapTime in self.snapList.iteritems():
                        snapYear = snapTime.split(' ')[0].split('/')[2]
                        if snapYear not in yearList:
                                yearList.append(snapYear)
                for year in sorted(yearList):
                        self.combo_beginSnapYear.append_text(year)
	
	def setEndSnapYear(self):
		self.combo_endSnapYear.get_model().clear()
		self.combo_endSnapYear.append_text(" "*self.len_combo_snapYear)
                yearList=[]
                for snapId, snapTime in self.snapList.iteritems():
                        snapYear = snapTime.split(' ')[0].split('/')[2]
                        if snapYear not in yearList:
                                yearList.append(snapYear)
                for year in sorted(yearList):
                        self.combo_endSnapYear.append_text(year)

	def setBeginSnapMonth(self, year=None):
		self.combo_beginSnapMonth.get_model().clear()
		self.combo_beginSnapMonth.append_text(" "*self.len_combo_snapMonth)
		self.combo_beginSnapMonth.set_active(0)
		if year != None:
			monthList=[]
			for snapId, snapTime in self.snapList.iteritems():
				snapDay, snapMonth, snapYear = snapTime.split(' ')[0].split('/')
				if snapYear == year and snapMonth not in monthList:
					monthList.append(snapMonth)
			for month in sorted(monthList):
				self.combo_beginSnapMonth.append_text(month)

	def setEndSnapMonth(self, year=None):
		self.combo_endSnapMonth.get_model().clear()
		self.combo_endSnapMonth.append_text(" "*self.len_combo_snapMonth)
		self.combo_endSnapMonth.set_active(0)
		if year != None:
			monthList=[]
			for snapId, snapTime in self.snapList.iteritems():
	                        snapDay, snapMonth, snapYear = snapTime.split(' ')[0].split('/')
	                        if snapYear == year and snapMonth not in monthList:
	                                monthList.append(snapMonth)
			for month in sorted(monthList):
	                        self.combo_endSnapMonth.append_text(month)

	def setBeginSnapDay(self, month=None, year=None):
		self.combo_beginSnapDay.get_model().clear()
		self.combo_beginSnapDay.append_text(" "*self.len_combo_snapDay)
		self.combo_beginSnapDay.set_active(0)
		if None not in (year, month):
			dayList=[]
			for snapId, snapTime in self.snapList.iteritems():
				snapDay, snapMonth, snapYear = snapTime.split(' ')[0].split('/')
				if snapYear == year and snapMonth == month and snapDay not in dayList:
					dayList.append(snapDay)
			for day in sorted(dayList):
				self.combo_beginSnapDay.append_text(day)

	def setEndSnapDay(self, month=None, year=None):
		self.combo_endSnapDay.get_model().clear()
		self.combo_endSnapDay.append_text(" "*self.len_combo_snapDay)
		self.combo_endSnapDay.set_active(0)
		if None not in (year, month):
                        dayList=[]
                        for snapId, snapTime in self.snapList.iteritems():
                                snapDay, snapMonth, snapYear = snapTime.split(' ')[0].split('/')
                                if snapYear == year and snapMonth == month and snapDay not in dayList:
                                        dayList.append(snapDay)
                        for day in sorted(dayList):
                                self.combo_endSnapDay.append_text(day)

	def setBeginSnapHour(self, day=None, month=None, year=None):
		self.combo_beginSnapHour.get_model().clear()
		self.combo_beginSnapHour.append_text(" "*self.len_combo_snapHour)
		self.combo_beginSnapHour.set_active(0)
		if None not in (year, month, day):
			hourList=[]
			for snapId, snapTime in self.snapList.iteritems():
				snapDay, snapMonth, snapYear = snapTime.split(' ')[0].split('/')
				snapHour, snapMinute = snapTime.split(' ')[1].split(':')
				if snapYear == year and snapMonth == month and snapDay == day and snapHour not in hourList:
					hourList.append(snapHour)
			for hour in sorted(hourList):	
				self.combo_beginSnapHour.append_text(hour)

	def setEndSnapHour(self, day=None, month=None, year=None):
		self.combo_endSnapHour.get_model().clear()
		self.combo_endSnapHour.append_text(" "*self.len_combo_snapHour)
		self.combo_endSnapHour.set_active(0)
		if None not in (year, month, day):
			hourList=[]
			for snapId, snapTime in self.snapList.iteritems():
				snapDay, snapMonth, snapYear = snapTime.split(' ')[0].split('/')
				snapHour, snapMinute = snapTime.split(' ')[1].split(':')
				if snapYear == year and snapMonth == month and snapDay == day and snapHour not in hourList:
					hourList.append(snapHour)
			for hour in sorted(hourList):
				self.combo_endSnapHour.append_text(hour)
	
	def setBeginSnapMinute(self, hour=None, day=None, month=None, year=None):
		self.combo_beginSnapMinute.get_model().clear()
		self.combo_beginSnapMinute.append_text(" "*self.len_combo_snapMinute)
		self.combo_beginSnapMinute.set_active(0)
		if None not in (year, month, day, hour):
			minuteList=[]
			for snapId, snapTime in self.snapList.iteritems():
				snapDay, snapMonth, snapYear = snapTime.split(' ')[0].split('/')
				snapHour, snapMinute = snapTime.split(' ')[1].split(':')
				if snapYear == year and snapMonth == month and snapDay == day and snapHour == hour and snapMinute not in minuteList:
					minuteList.append(snapMinute)
			for minute in sorted(minuteList):
				self.combo_beginSnapMinute.append_text(minute)

	def setEndSnapMinute(self, hour=None, day=None, month=None, year=None):
		self.combo_endSnapMinute.get_model().clear()
		self.combo_endSnapMinute.append_text(" "*self.len_combo_snapMinute)
		self.combo_endSnapMinute.set_active(0)
		if None not in (year, month, day, hour):
			minuteList=[]
			for snapId, snapTime in self.snapList.iteritems():
				snapDay, snapMonth, snapYear = snapTime.split(' ')[0].split('/')
				snapHour, snapMinute = snapTime.split(' ')[1].split(':')
				if snapYear == year and snapMonth == month and snapDay == day and snapHour == hour and snapMinute not in minuteList:
					minuteList.append(snapMinute)
			for minute in sorted(minuteList):
				self.combo_endSnapMinute.append_text(minute)


	def changeBeginSnapYear(self, beginSnapList):
		modele_year = self.combo_beginSnapYear.get_model()
		index_year = self.combo_beginSnapYear.get_active()
		if index_year > 0 and modele_year[index_year][0].strip() != "":
			self.setBeginSnapMonth(modele_year[index_year][0])
			self.setBeginSnapDay()
			self.setBeginSnapHour()
			self.setBeginSnapMinute()

	def changeEndSnapYear(self, endSnapList):
		modele_year = self.combo_endSnapYear.get_model()
		index_year = self.combo_endSnapYear.get_active()
		if index_year > 0 and modele_year[index_year][0].strip() != "":
			self.setEndSnapMonth(modele_year[index_year][0])
			self.setEndSnapDay()
			self.setEndSnapHour()
			self.setEndSnapMinute()

	def changeBeginSnapMonth(self, beginSnapList):
		modele_year = self.combo_beginSnapYear.get_model()
		index_year = self.combo_beginSnapYear.get_active()
		modele_month = self.combo_beginSnapMonth.get_model()
		index_month = self.combo_beginSnapMonth.get_active()
		if index_month > 0 and modele_month[index_month][0].strip() != "":
			self.setBeginSnapDay(modele_month[index_month][0], modele_year[index_year][0])
			self.setBeginSnapHour()
			self.setBeginSnapMinute()

	def changeEndSnapMonth(self, endSnapList):
		modele_year = self.combo_endSnapYear.get_model()
		index_year = self.combo_endSnapYear.get_active()
		modele_month = self.combo_endSnapMonth.get_model()
		index_month = self.combo_endSnapMonth.get_active()
		if index_month > 0 and modele_month[index_month][0].strip() != "":
			self.setEndSnapDay(modele_month[index_month][0], modele_year[index_year][0])
			self.setEndSnapHour()
			self.setEndSnapMinute()

	def changeBeginSnapDay(self, beginSnapList):
		modele_year = self.combo_beginSnapYear.get_model()
		index_year = self.combo_beginSnapYear.get_active()
		modele_month = self.combo_beginSnapMonth.get_model()
		index_month = self.combo_beginSnapMonth.get_active()
		modele_day = self.combo_beginSnapDay.get_model()
		index_day = self.combo_beginSnapDay.get_active()
		if index_day > 0 and modele_day[index_day][0].strip() != "":
			self.setBeginSnapHour(modele_day[index_day][0], modele_month[index_month][0], modele_year[index_year][0])
			self.setBeginSnapMinute()

	def changeEndSnapDay(self, endSnapList):
		modele_year = self.combo_endSnapYear.get_model()
		index_year = self.combo_endSnapYear.get_active()
		modele_month = self.combo_endSnapMonth.get_model()
		index_month = self.combo_endSnapMonth.get_active()
		modele_day = self.combo_endSnapDay.get_model()
		index_day = self.combo_endSnapDay.get_active()
		if index_day > 0 and modele_day[index_day][0].strip() != "":
			self.setEndSnapHour(modele_day[index_day][0], modele_month[index_month][0], modele_year[index_year][0])
			self.setEndSnapMinute()

	def changeBeginSnapHour(self, beginSnapList):
		modele_year = self.combo_beginSnapYear.get_model()
		index_year = self.combo_beginSnapYear.get_active()
		modele_month = self.combo_beginSnapMonth.get_model()
		index_month = self.combo_beginSnapMonth.get_active()
		modele_day = self.combo_beginSnapDay.get_model()
		index_day = self.combo_beginSnapDay.get_active()
		modele_hour = self.combo_beginSnapHour.get_model()
		index_hour = self.combo_beginSnapHour.get_active()
		if index_hour > 0 and modele_hour[index_hour][0].strip() != "":
			self.setBeginSnapMinute(modele_hour[index_hour][0], modele_day[index_day][0], modele_month[index_month][0], modele_year[index_year][0])

        def changeEndSnapHour(self, endSnapList):
		modele_year = self.combo_endSnapYear.get_model()
		index_year = self.combo_endSnapYear.get_active()
		modele_month = self.combo_endSnapMonth.get_model()
		index_month = self.combo_endSnapMonth.get_active()
		modele_day = self.combo_endSnapDay.get_model()
		index_day = self.combo_endSnapDay.get_active()
		modele_hour = self.combo_endSnapHour.get_model()
		index_hour = self.combo_endSnapHour.get_active()
		if index_hour > 0 and modele_hour[index_hour][0].strip() != "":
			self.setEndSnapMinute(modele_hour[index_hour][0], modele_day[index_day][0], modele_month[index_month][0], modele_year[index_year][0])

	def changeBeginSnapMinute(self, beginSnapList):
                return

        def changeEndSnapMinute(self, endSnapList):
                return


	def setSnapList(self):
		req = "select distinct snap_id, to_char(begin_interval_time, 'dd/mm/yy hh24:mi') begin from dba_hist_snapshot order by 1"
		res = self.oTool.execSelect(req, False)
		for elem in res:
			self.snapList[elem[0]]=elem[1]

	def setInstanceList(self):
		req = "select instance_name from gv$instance"
		res = self.oTool.execSelect(req, False)
		for elem in res:
			self.instanceList[elem[0]]=False

	def generateSpReport(self, widget):
		modele_year = self.combo_beginSnapYear.get_model()
		index_year = self.combo_beginSnapYear.get_active()
		modele_month = self.combo_beginSnapMonth.get_model()
		index_month = self.combo_beginSnapMonth.get_active()
		modele_day = self.combo_beginSnapDay.get_model()
		index_day = self.combo_beginSnapDay.get_active()
		modele_hour = self.combo_beginSnapHour.get_model()
		index_hour = self.combo_beginSnapHour.get_active()
		modele_minute = self.combo_beginSnapMinute.get_model()
		index_minute = self.combo_beginSnapMinute.get_active()
		beginTime = [modele_year[index_year][0], modele_month[index_month][0], modele_day[index_day][0], modele_hour[index_hour][0], modele_minute[index_minute][0]]

		modele_year = self.combo_endSnapYear.get_model()
		index_year = self.combo_endSnapYear.get_active()
		modele_month = self.combo_endSnapMonth.get_model()
		index_month = self.combo_endSnapMonth.get_active()
		modele_day = self.combo_endSnapDay.get_model()
		index_day = self.combo_endSnapDay.get_active()
		modele_hour = self.combo_endSnapHour.get_model()
		index_hour = self.combo_endSnapHour.get_active()
		modele_minute = self.combo_endSnapMinute.get_model()
		index_minute = self.combo_endSnapMinute.get_active()
		endTime = [modele_year[index_year][0], modele_month[index_month][0], modele_day[index_day][0], modele_hour[index_hour][0], modele_minute[index_minute][0]]

		for ind in range(10):
			if beginTime[ind] != endTime[ind]:
				if beginTime[ind] > endTime[ind] or beginTime[ind].strip() == '' or endTime[ind].strip() == '':
					self.error_dialog("\nRange-Error-Message:\nLa date de début du rapport doit être antérieur à la date de fin du rapport.")
					return
				elif beginTime[ind] < endTime[ind]:
					break
		mailForm = self.entry_mail.get_text()
		mailList = mailForm.replace(',',';').strip().split(';')
		if len(mailList) == 0:
			self.error_dialog("\nStatspack-Warning-Message:\nAucune adresse mail n'a été saisie.")
			return
		checkedInst=False
		reportList=[]
		for inst, checked in self.instanceList.iteritems():
			if checked:
				checkedInst=True
				cmd = "../lib/genSpRep.sh -d "+inst+" -s "+str(beginTime[2])+str(beginTime[1])+str(beginTime[3])+str(beginTime[4])+" -e "+str(endTime[2])+str(endTime[1])+str(endTime[3])+str(endTime[4])+" -u "+self.oTool.user+" -p "+self.oTool.password
				res = os.popen(cmd)
				content = res.read()
				reportList.append(content.split('End of Report ( ')[1].split(' )')[0])
		if not checkedInst:
			self.warn_dialog("\nStatspack-Warning-Message:\nAucune instance n'a été sélectionnée.")
		if len(reportList) > 0:
			# MAIL
			self.tools=Tools.Tools()
			self.tools.sendMailWithAttachment("jlambert@sigma.fr",mailList,"Statspack Report "+self.oTool.base, "Contenu en piece-jointe", reportList)
			for report in reportList:
				os.remove(report)
			self.notif_dialog("\nStatspack-Info-Message:\nRapport(s) statspack envoyé(s) à "+", ".join(mailList))


	def close_window(self, widget, data=None):
		self.fenetre.destroy()

