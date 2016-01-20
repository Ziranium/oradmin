#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Jonathan LAMBERT"

from openpyxl import Workbook
from openpyxl.styles import Style, PatternFill, Border, Side, Alignment, Protection, Font

import pygtk
pygtk.require('2.0')
import gtk

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))

from Window import Window
from Window_result import Window_result
from Window_statspack import Window_statspack

import Queue
import time

from builtList import _DBLIST, _REGISTEREDQUERY
import Tools
import OraTool
import OracleThread

class TableDBLine():
	def __init__(self, indexLine, but_connect, but_disconnect, but_statspack, combo_dbList, combo_db, combo_dbUser):
		self.len_label_empty = 6
		self.indexLine = indexLine
		self.but_connect=but_connect
		self.but_disconnect=but_disconnect
		self.but_statspack=but_statspack
		self.combo_dbList=combo_dbList
		self.combo_db=combo_db
		self.combo_dbUser=combo_dbUser
		self.label_dbList = gtk.Label("Liste de bases : ")
		self.label_dbList.set_alignment(xalign=0.0, yalign=0.5)
		self.label_db = gtk.Label("Bases : ")
		self.label_db.set_alignment(xalign=0.0, yalign=0.5)
		self.label_dbUser = gtk.Label("Utilisateur : ")
		self.label_dbUser.set_alignment(xalign=0.0, yalign=0.5)
		self.label_empty = gtk.Label(" "*self.len_label_empty)
		self.label_empty.set_alignment(xalign=0.0, yalign=0.5)
		self.label_empty2 = gtk.Label(" "*self.len_label_empty)
		self.label_empty2.set_alignment(xalign=0.0, yalign=0.5)

class Window_main(Window):
	def __init__(self):
		self.tools=Tools.Tools()
		self.oraTools={}
		self.tabDBline=[]
		self.filles = []
		## ITEM PARAM
		self.len_combo_top = 40
		self.len_combo_mid = 40
		self.len_entry_query = 100
		## FENETRE
		Window.__init__(self, "Administration Oracle")
		self.fenetre.connect("delete_event", self.close_main)
		settings = gtk.settings_get_default()
		settings.props.gtk_button_images = True
		self.vbox_main=gtk.VBox(False, 0)
		self.fenetre.add(self.vbox_main)
		self.set_xml_menu()
		self.hbox_top = gtk.HBox(False, 0)
		self.vbox_sep1 = gtk.VBox(False, 0)
		self.hbox_mid = gtk.HBox(False, 0)
		self.vbox_sep2 = gtk.VBox(False, 0)
		self.hbox_bot = gtk.HBox(True, 0)
		self.vbox_main.pack_start(self.hbox_top, False, False, 30)
		self.vbox_main.pack_start(self.vbox_sep1, False, False, 0)
		self.vbox_main.pack_start(self.hbox_mid, False, False, 30)
		self.vbox_main.pack_start(self.vbox_sep2, False, False, 0)
		self.vbox_main.pack_start(self.hbox_bot, False, False, 30)
		## STOCK ITEM
		self.stock_items = (
		("gtk-connectDB", "", 0, 0, None),
		("gtk-disconnectDB", "", 0, 0, None),
		("gtk-addConnection", "", 0, 0, None),
		("gtk-playQuery", "", 0, 0, None),
		("gtk-spreport", "", 0, 0, None),
		)
		self.stock_aliases = (
		("gtk-connectDB", gtk.STOCK_CONNECT),
		("gtk-disconnectDB", gtk.STOCK_DISCONNECT),
		("gtk-addConnection", gtk.STOCK_ADD),
		("gtk-playQuery", gtk.STOCK_MEDIA_PLAY),
		("gtk-spreport", gtk.STOCK_PROPERTIES),
		)
		gtk.stock_add(self.stock_items)
		factory = gtk.IconFactory()
		factory.add_default()
		style = gtk.Style()
		for item, alias in self.stock_aliases:
			icon_set = style.lookup_icon_set(alias)
			factory.add(item, icon_set)

		## vbox_sep
		self.frame_sep1=gtk.Frame("")
		self.frame_sep2=gtk.Frame("")
		self.vbox_sep1.pack_start(self.frame_sep1, False, False, 5)
		self.vbox_sep2.pack_start(self.frame_sep2, False, False, 5)

		self.tab_form = gtk.Table(1, 11, False)
		self.hbox_top.pack_start(self.tab_form, False, False, 0)

		# Add Line
		self.but_addLine=gtk.Button(stock="gtk-addConnection")
                self.but_addLine.modify_bg(gtk.STATE_NORMAL, self.but_color)
                self.but_addLine.connect("clicked", self.addConnectionLine)
                self.but_addLine.set_sensitive(True)

		# combo box dbList
		combo_dbList=gtk.combo_box_new_text()
		combo_dbList.modify_bg(gtk.STATE_NORMAL, self.but_color)
		combo_dbList.append_text(" "*self.len_combo_top)
		for dbList in _DBLIST.keys():
			combo_dbList.append_text(dbList)
		combo_dbList.connect('changed', self.changeDbList, 0)

		# combo box db
		combo_db=gtk.combo_box_new_text()
		combo_db.modify_bg(gtk.STATE_NORMAL, self.but_color)
		combo_db.append_text(" "*self.len_combo_top)
		combo_db.connect('changed', self.changeDb, 0)

		# combo box dbUser
		combo_dbUser=gtk.combo_box_new_text()
		combo_dbUser.modify_bg(gtk.STATE_NORMAL, self.but_color)
		combo_dbUser.append_text(" "*self.len_combo_top)
		combo_dbUser.connect('changed', self.changeDbUser, 0)

		# Connexion
		but_connect=gtk.Button(stock="gtk-connectDB")
		but_connect.modify_bg(gtk.STATE_NORMAL, self.but_color)
		but_connect.connect("clicked", self.connectDb, 0)
		but_connect.set_sensitive(False)

		# Deconnexion
		but_disconnect=gtk.Button(stock="gtk-disconnectDB")
                but_disconnect.modify_bg(gtk.STATE_NORMAL, self.but_color)
                but_disconnect.connect("clicked", self.disconnectDb, 0)

		# Statspack
		but_statspack=gtk.Button(stock="gtk-spreport")
		but_statspack.modify_bg(gtk.STATE_NORMAL, self.but_color)
		but_statspack.connect("clicked", self.generateSpreport, 0)

		# Tab DB line
		self.tabDBline.append(TableDBLine(0, but_connect, but_disconnect, but_statspack, combo_dbList, combo_db, combo_dbUser))
		self.tab_form.attach(self.but_addLine, 0, 1, 0, 1)
		self.tab_form.attach(self.tabDBline[0].label_dbList, 1, 2, 0, 1)
		self.tab_form.attach(self.tabDBline[0].combo_dbList, 2, 3, 0, 1)
		self.tab_form.attach(self.tabDBline[0].label_empty, 3, 4, 0, 1)
		self.tab_form.attach(self.tabDBline[0].label_db, 4, 5, 0, 1)
		self.tab_form.attach(self.tabDBline[0].combo_db, 5, 6, 0, 1)
		self.tab_form.attach(self.tabDBline[0].label_empty2, 6, 7, 0, 1)
		self.tab_form.attach(self.tabDBline[0].label_dbUser, 7, 8, 0, 1)
		self.tab_form.attach(self.tabDBline[0].combo_dbUser, 8, 9, 0, 1)
		self.tab_form.attach(self.tabDBline[0].but_connect, 9, 10, 0, 1)
		self.tab_form.attach(self.tabDBline[0].but_disconnect, 10, 11, 0, 1)
		self.tab_form.attach(self.tabDBline[0].but_statspack, 11, 12, 0, 1)

		## Query Box

		# Frame Query
		self.frm_query=gtk.Frame("Requête libre")
		self.frm_registeredQuery=gtk.Frame("Requête pré-fabriquée")
		self.frm_parameter=gtk.Frame("Paramètre")

		# Query Button
		self.but_query=gtk.Button(stock="gtk-playQuery")
                self.but_query.modify_bg(gtk.STATE_NORMAL, self.but_color)
                self.but_query.connect("clicked", self.execQuery, "query")

		# Query Text
		self.entry_query = gtk.Entry()
		self.entry_query.set_width_chars(self.len_entry_query)

		# RegisteredQuery Button
		self.but_registeredQuery=gtk.Button(stock="gtk-playQuery")
		self.but_registeredQuery.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.but_registeredQuery.connect("clicked", self.execQuery, "registered")
		self.but_registeredQuery.set_sensitive(False)

		# RegisteredQuery combobox
		self.combo_registeredQuery=gtk.combo_box_new_text()
		self.combo_registeredQuery.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.combo_registeredQuery.append_text(" "*self.len_combo_mid)
		for queryName in _REGISTEREDQUERY.keys():
                        self.combo_registeredQuery.append_text(queryName)
                self.combo_registeredQuery.connect('changed', self.changeRegisteredQuery)

		# Parameter Text
		self.entry_parameter = gtk.Entry()
		self.entry_parameter.set_width_chars(self.len_entry_query)

		# Parameter Button
		self.but_parameter=gtk.Button(stock="gtk-playQuery")
		self.but_parameter.modify_bg(gtk.STATE_NORMAL, self.but_color)
		self.but_parameter.connect("clicked", self.execQuery, "parameter")

		self.tab_query_global = gtk.Table(1, 5, False)
		label_empty = gtk.Label(" ")
		label_empty.set_alignment(xalign=0.0, yalign=0.5)
		label_empty2 = gtk.Label(" ")
		label_empty2.set_alignment(xalign=0.0, yalign=0.5)
		self.hbox_mid.pack_start(self.tab_query_global, False, False, 0)
		self.tab_query_global.attach(self.frm_query, 0, 1, 0, 1)
		self.tab_query_global.attach(label_empty, 0, 1, 1, 2)
		self.tab_query_global.attach(self.frm_registeredQuery, 0, 1, 2, 3)
		self.tab_query_global.attach(label_empty2, 0, 1, 3, 4)
		self.tab_query_global.attach(self.frm_parameter, 0, 1, 4, 5)
		self.tab_query_query = gtk.Table(2, 1, False)
		self.tab_query_registeredQuery = gtk.Table(2, 1, False)
		self.tab_query_parameter = gtk.Table(2, 1, False)
		self.frm_query.add(self.tab_query_query)
		self.frm_registeredQuery.add(self.tab_query_registeredQuery)
		self.frm_parameter.add(self.tab_query_parameter)
		self.tab_query_query.attach(self.but_query, 0, 1, 0, 1)
		self.tab_query_query.attach(self.entry_query, 1, 2, 0, 1)
		self.tab_query_registeredQuery.attach(self.but_registeredQuery, 0, 1, 0, 1)
		self.tab_query_registeredQuery.attach(self.combo_registeredQuery, 1, 2, 0, 1)
		self.tab_query_parameter.attach(self.but_parameter, 0, 1, 0, 1)
		self.tab_query_parameter.attach(self.entry_parameter, 1, 2, 0, 1)

		# ProgressBar
		self.progressBar_workingSQL = gtk.ProgressBar()
		self.progressBar_workingSQL.set_size_request(400,-1)
		self.hbox_bot.pack_start(self.progressBar_workingSQL, False, False, 0)
		self.progressBar_workingSQL.set_fraction(0)

		## SHOW
		self.fenetre.show_all()

		## Resize
		sizeCombo = self.entry_parameter.size_request()
		self.combo_registeredQuery.set_size_request(sizeCombo[0],sizeCombo[1])

		## HIDE
		self.tabDBline[0].but_disconnect.hide()
		self.tabDBline[0].but_statspack.hide()


	def close_main(self, widget, evenement):
		gtk.main_quit()
		return False
		
	def set_xml_menu(self):
		self.menu_xml='''<ui>
		<menubar name="MenuBar">
			<menu action="Fichier">
				<menuitem action="Nouveau"/>
				<menuitem action="Ouvrir"/>
				<menuitem action="Enregistrer"/>
				<separator/>
				<menuitem action="Quitter"/>
			</menu>
			<menu action="Edition">
				<menuitem action="Rechercher"/>
			</menu>
			<menu action="?">
				<menuitem action="Aide"/>
				<menuitem action="A propos"/>
			</menu>
		</menubar>
		</ui>'''
		self.uimanager = gtk.UIManager()
		self.actiongroup = gtk.ActionGroup('UIManager')
		self.actiongroup.add_actions([('Quitter', gtk.STOCK_QUIT, '_Quitter', "<Control>q",
						'Quit the Program', self.menu_fichier_quitter),
						('Nouveau', gtk.STOCK_NEW, '_Nouveau', "<Control>n",
						'Nouveau', self.menu_fichier_nouveau),
						('Ouvrir', gtk.STOCK_OPEN, '_Ouvrir', "<Control>o",
						'Ouvrir', self.menu_fichier_ouvrir),
						('Enregistrer', gtk.STOCK_SAVE, 'Enregi_strer', "<Control>s",
						'Enregistrer', self.menu_fichier_enregistrer),
						('Rechercher', gtk.STOCK_FIND, 'Rechercher', "<Control>f",
						'Rechercher', self.menu_edition_rechercher),
						('Aide', gtk.STOCK_HELP, '_Aide', "<Control>h",
						'Aide', self.menu_about_aide),
						('A propos', gtk.STOCK_ABOUT, 'A _Propos', "<Control>p",
						'A propos', self.menu_about_aPropos),
						('Fichier', None, 'Fichier'),
						('Edition', None, 'Edition'),
						('?', None, '?')])
		self.accelgroup = self.uimanager.get_accel_group()
		self.fenetre.add_accel_group(self.accelgroup)
		self.uimanager.insert_action_group(self.actiongroup, 0)
		self.uimanager.add_ui_from_string(self.menu_xml)
		self.menubar = self.uimanager.get_widget('/MenuBar')
		self.vbox_main.pack_start(self.menubar, False, False, 0)

	def menu_fichier_nouveau(self, widget):
		print "Fichier / Nouveau"
	
	def menu_fichier_ouvrir(self, widget):
		print "Fichier / Ouvrir"
	
	def menu_fichier_enregistrer(self, widget):
		print "Fichier / Enregistrer"
	
	def menu_fichier_quitter(self, widget):
		gtk.main_quit()

	def menu_edition_rechercher(self, widget):
		print "Options / Rechercher"

	def menu_about_aide(self, widget):
		print "? / Aide"
		dialog = gtk.MessageDialog(
		parent         = None,
		flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
		type           = gtk.MESSAGE_INFO,
		buttons        = gtk.BUTTONS_OK,
		message_format = "Une documentation technique illustrée est disponible sur : http://wiki.groupesigma.fr/index.php/XSYS_oradmin")
		dialog.set_title('A propos de Oradmin')
		dialog.connect('response', lambda dialog, response: dialog.destroy())
		dialog.show_all()

	def menu_about_aPropos(self, widget):
		dialog = gtk.MessageDialog(
		parent         = None,
		flags          = gtk.DIALOG_DESTROY_WITH_PARENT,
		type           = gtk.MESSAGE_INFO,
		buttons        = gtk.BUTTONS_OK,
		message_format = "Version : 0.3\nAuteur : Jonathan LAMBERT\nDerniere Modification : 17/11/2015")
		dialog.set_title('A propos de Oradmin')
		color = gtk.gdk.color_parse('#FFFFFF')
		dialog.modify_bg(gtk.STATE_NORMAL, color)
		dialog.connect('response', lambda dialog, response: dialog.destroy())
		dialog.show()

	def changeDbList(self, listDb, indexLine):
		modele = listDb.get_model()
		index = listDb.get_active()
		if index > 0 and modele[index][0].strip() != "":
			self.tabDBline[indexLine].combo_db.get_model().clear()
			res_db=_DBLIST[modele[index][0]]
			self.tabDBline[indexLine].combo_db.append_text(" "*self.len_combo_top)
			self.tabDBline[indexLine].combo_db.append_text("ALL")
			for db in res_db:
				self.tabDBline[indexLine].combo_db.append_text(db)
			modWidth = 1+len(res_db) / 15
			self.tabDBline[indexLine].combo_db.set_wrap_width(modWidth)
			self.tabDBline[indexLine].combo_db.set_active(0)

	def changeDb(self, db, indexLine):
		modele = db.get_model()
		index = db.get_active()
		if index > 0 and modele[index][0].strip() != "":
			self.tabDBline[indexLine].combo_dbUser.get_model().clear()
			if modele[index][0].strip() == "ALL":
				modele_dbList = self.tabDBline[indexLine].combo_dbList.get_model()
				index_dbList = self.tabDBline[indexLine].combo_dbList.get_active()
				res_dbUser=self.tools.getUserDBCommon(_DBLIST[modele_dbList[index_dbList][0]])
			else:
				res_dbUser=self.tools.getUserDB(modele[index][0])
			self.tabDBline[indexLine].combo_dbUser.append_text(" "*self.len_combo_top)
			for user in res_dbUser:
				self.tabDBline[indexLine].combo_dbUser.append_text(user)
			self.tabDBline[indexLine].combo_dbUser.set_active(0)
		elif index <= 0:
			self.tabDBline[indexLine].combo_dbUser.get_model().clear()
			self.tabDBline[indexLine].combo_dbUser.append_text(" "*self.len_combo_top)
			self.tabDBline[indexLine].combo_dbUser.set_active(0)

	def changeDbUser(self, user, indexLine):
		modele = user.get_model()
		index = user.get_active()
		if index > 0 and modele[index][0].strip() != "":
			self.tabDBline[indexLine].but_connect.set_sensitive(True)
		elif index <= 0:
			self.tabDBline[indexLine].but_connect.set_sensitive(False)

	def changeRegisteredQuery(self, registeredQuery):
		modele = registeredQuery.get_model()
		index = registeredQuery.get_active()
		if index > 0 and modele[index][0].strip() != "":
			self.but_registeredQuery.set_sensitive(True)
		elif index <= 0:
			self.but_registeredQuery.set_sensitive(False)


	def connectDb(self, widget, indexLine):
		modele_db = self.tabDBline[indexLine].combo_db.get_model()
		index_db = self.tabDBline[indexLine].combo_db.get_active()
		modele_dbUser = self.tabDBline[indexLine].combo_dbUser.get_model()
		index_dbUser = self.tabDBline[indexLine].combo_dbUser.get_active()
		if index_dbUser > 0 and modele_dbUser[index_dbUser][0].strip() != "":
			if modele_db[index_db][0].strip() == "ALL":
				modele_dbList = self.tabDBline[indexLine].combo_dbList.get_model()
				index_dbList = self.tabDBline[indexLine].combo_dbList.get_active()
				for dbName in _DBLIST[modele_dbList[index_dbList][0]]:
					pw=self.tools.getPass(dbName, modele_dbUser[index_dbUser][0])
					self.oraTools[dbName] = OraTool.OraTool(dbName, modele_dbUser[index_dbUser][0], pw)
					self.oraTools[dbName].connect()
				if self.oraTools[dbName].connected():
					self.tabDBline[indexLine].but_connect.set_sensitive(False)
					self.tabDBline[indexLine].combo_dbList.set_sensitive(False)
					self.tabDBline[indexLine].combo_db.set_sensitive(False)
					self.tabDBline[indexLine].combo_dbUser.set_sensitive(False)
					self.tabDBline[indexLine].but_disconnect.set_sensitive(True)
					self.tabDBline[indexLine].but_disconnect.show()
			else:
				pw=self.tools.getPass(modele_db[index_db][0], modele_dbUser[index_dbUser][0])
				self.oraTools[modele_db[index_db][0]] = OraTool.OraTool(modele_db[index_db][0], modele_dbUser[index_dbUser][0], pw)
				self.oraTools[modele_db[index_db][0]].connect()
				if self.oraTools[modele_db[index_db][0]].connected():
					self.tabDBline[indexLine].but_connect.set_sensitive(False)
					self.tabDBline[indexLine].combo_dbList.set_sensitive(False)
					self.tabDBline[indexLine].combo_db.set_sensitive(False)
					self.tabDBline[indexLine].combo_dbUser.set_sensitive(False)
					self.tabDBline[indexLine].but_disconnect.set_sensitive(True)
					self.tabDBline[indexLine].but_disconnect.show()
					self.tabDBline[indexLine].but_statspack.set_sensitive(True)
					self.tabDBline[indexLine].but_statspack.show()

	def disconnectDb(self, widget, indexLine):
		modele_db = self.tabDBline[indexLine].combo_db.get_model()
                index_db = self.tabDBline[indexLine].combo_db.get_active()
                modele_dbUser = self.tabDBline[indexLine].combo_dbUser.get_model()
                index_dbUser = self.tabDBline[indexLine].combo_dbUser.get_active()
		if modele_db[index_db][0].strip() == "ALL":
			modele_dbList = self.tabDBline[indexLine].combo_dbList.get_model()
			index_dbList = self.tabDBline[indexLine].combo_dbList.get_active()
			allDisconnected=True
			for dbName in _DBLIST[modele_dbList[index_dbList][0]]:
				try:
					self.oraTools[dbName].disconnect()
				except:
					self.warn_dialog("La connexion a la base "+dbName+" avec l'utilisateur "+self.oraTools[dbName].user+" n'etait déjà plus active.")
				if self.oraTools[dbName].connected():
					allDisconnected=False
			if allDisconnected:
				self.tabDBline[indexLine].but_connect.set_sensitive(True)
				self.tabDBline[indexLine].combo_dbList.set_sensitive(True)
				self.tabDBline[indexLine].combo_db.set_sensitive(True)
				self.tabDBline[indexLine].combo_dbUser.set_sensitive(True)
				self.tabDBline[indexLine].but_disconnect.set_sensitive(False)
				self.tabDBline[indexLine].but_statspack.set_sensitive(False)
		else:
			try:
				self.oraTools[modele_db[index_db][0]].disconnect()
			except:
				self.warn_dialog("La connexion a la base "+self.oraTools[modele_db[index_db][0]].base+" avec l'utilisateur "+self.oraTools[modele_db[index_db][0]].user+" n'etait déjà plus active.")
			if not self.oraTools[modele_db[index_db][0]].connected():
				self.tabDBline[indexLine].but_connect.set_sensitive(True)
				self.tabDBline[indexLine].combo_dbList.set_sensitive(True)
				self.tabDBline[indexLine].combo_db.set_sensitive(True)
				self.tabDBline[indexLine].combo_dbUser.set_sensitive(True)
				self.tabDBline[indexLine].but_disconnect.set_sensitive(False)
				self.tabDBline[indexLine].but_statspack.set_sensitive(False)

	def generateSpreport(self, widget, indexLine):
		modele_db = self.tabDBline[indexLine].combo_db.get_model()
		index_db = self.tabDBline[indexLine].combo_db.get_active()
		dbName = modele_db[index_db][0]
		self.filles.append(Window_statspack(self, self.oraTools[dbName]))

		
	def addConnectionLine(self, widget=None):

		# New Size tab_form
		numRows = self.tab_form.get_property('n-rows')
		numCol = self.tab_form.get_property('n-columns')
		self.tab_form.resize(numRows+1, numCol)
		
		# combo box dbList
		combo_dbList=gtk.combo_box_new_text()
		combo_dbList.modify_bg(gtk.STATE_NORMAL, self.but_color)
		combo_dbList.append_text(" "*self.len_combo_top)
		for dbList in _DBLIST.keys():
			combo_dbList.append_text(dbList)
		combo_dbList.connect('changed', self.changeDbList, numRows)
		
		# combo box db
		combo_db=gtk.combo_box_new_text()
		combo_db.modify_bg(gtk.STATE_NORMAL, self.but_color)
		combo_db.append_text(" "*self.len_combo_top)
		combo_db.connect('changed', self.changeDb, numRows)
		
		# combo box dbUser
		combo_dbUser=gtk.combo_box_new_text()
		combo_dbUser.modify_bg(gtk.STATE_NORMAL, self.but_color)
		combo_dbUser.append_text(" "*self.len_combo_top)
		combo_dbUser.connect('changed', self.changeDbUser, numRows)
		
		# Connexion
		but_connect=gtk.Button(stock="gtk-connectDB")
		but_connect.modify_bg(gtk.STATE_NORMAL, self.but_color)
		but_connect.connect("clicked", self.connectDb, numRows)
		but_connect.set_sensitive(False)
		
		# Deconnexion
		but_disconnect=gtk.Button(stock="gtk-disconnectDB")
		but_disconnect.modify_bg(gtk.STATE_NORMAL, self.but_color)
		but_disconnect.connect("clicked", self.disconnectDb, numRows)

		# Statspack
		but_statspack=gtk.Button(stock="gtk-spreport")
		but_statspack.modify_bg(gtk.STATE_NORMAL, self.but_color)
		but_statspack.connect("clicked", self.generateSpreport, 0)

		# Tab line
		self.tabDBline.append(TableDBLine(numRows, but_connect, but_disconnect, but_statspack, combo_dbList, combo_db, combo_dbUser))
		
		# Attach tab
		self.tab_form.attach(self.tabDBline[-1].label_dbList, 1, 2, numRows, numRows+1)
		self.tab_form.attach(self.tabDBline[-1].combo_dbList, 2, 3, numRows, numRows+1)
		self.tab_form.attach(self.tabDBline[-1].label_empty, 3, 4, numRows, numRows+1)
		self.tab_form.attach(self.tabDBline[-1].label_db, 4, 5, numRows, numRows+1)
		self.tab_form.attach(self.tabDBline[-1].combo_db, 5, 6, numRows, numRows+1)
		self.tab_form.attach(self.tabDBline[-1].label_empty2, 6, 7, numRows, numRows+1)
		self.tab_form.attach(self.tabDBline[-1].label_dbUser, 7, 8, numRows, numRows+1)
		self.tab_form.attach(self.tabDBline[-1].combo_dbUser, 8, 9, numRows, numRows+1)
		self.tab_form.attach(self.tabDBline[-1].but_connect, 9, 10, numRows, numRows+1)
		self.tab_form.attach(self.tabDBline[-1].but_disconnect, 10, 11, numRows, numRows+1)
		self.tab_form.attach(self.tabDBline[-1].but_statspack, 11, 12, numRows, numRows+1)

		# SHOW / HIDE
		self.tabDBline[-1].label_dbList.show()
		self.tabDBline[-1].combo_dbList.show()
		self.tabDBline[-1].label_empty.show()
		self.tabDBline[-1].label_db.show()
		self.tabDBline[-1].combo_db.show()
		self.tabDBline[-1].label_empty2.show()
		self.tabDBline[-1].label_dbUser.show()
		self.tabDBline[-1].combo_dbUser.show()
		self.tabDBline[-1].but_connect.show()
		
	def threadingQuery(self, req):
		dictRes = {}
		# Multithreading
		threads = []
		threadMax = 2
		outputQueue = Queue.Queue()
		queueLock = OracleThread.threading.Lock()
		inputQueue = Queue.Queue()
		queueLock.acquire()
		for threadID in range(threadMax):
			thread = OracleThread.Thread(threadID, inputQueue, outputQueue, queueLock, req)
			thread.start()
			threads.append(thread)
		for dbName, otool in self.oraTools.iteritems():
			if otool.connected():
				inputQueue.put(self.oraTools[dbName])
		# maj progressBar
		self.progressBar_workingSQL.set_text("Executing ...")
		qSize = qSizeMax = inputQueue.qsize()
		queueLock.release()
		while not inputQueue.empty():
			newSize = inputQueue.qsize()
			if newSize < qSize:
				#print "progression : "+str(qSize)
				self.progressBar_workingSQL.set_fraction((1.0/qSizeMax)*(qSizeMax-newSize))
				while gtk.events_pending():
					gtk.main_iteration()
				qSize = newSize
			pass
		self.progressBar_workingSQL.set_fraction(1.0)
		self.progressBar_workingSQL.set_text("Completed")
		for t in threads:
			t.exitFlag = True
			t.join()
		while not outputQueue.empty():
			#time.sleep(0.2)
			resTmp = outputQueue.get()
			if resTmp[resTmp.keys()[0]][0] == "ERROR":
				error, = resTmp[resTmp.keys()[0]][1].args
				self.error_dialog("\nOracle-Error-Message:\n"+error.message)
			else:
				dictRes.update(resTmp)
			#dictRes.update(outputQueue.get())
		return dictRes

	
	def execQuery(self, widget, queryType):
		if queryType == "query":
			req = self.entry_query.get_text().strip()
		elif queryType == "parameter":
			req = "select name, value from v$parameter where name='"+self.entry_parameter.get_text().strip().lower()+"'"
		elif queryType == "registered":
			modele_registeredQuery = self.combo_registeredQuery.get_model()
			index_registeredQuery = self.combo_registeredQuery.get_active()
			req = _REGISTEREDQUERY[modele_registeredQuery[index_registeredQuery][0]]
		if req != "":
			if req[-1] == ";":
				req = req[:-1]
			dictRes = self.threadingQuery(req)
			if dictRes != {}:
				self.filles.append(Window_result(self, dictRes))
			else:
				self.warn_dialog("Aucun résultat à afficher.")
		

def boucle():
    gtk.main()

if __name__ == "__main__":
    fenetre_principale = Window_main()
    boucle()

