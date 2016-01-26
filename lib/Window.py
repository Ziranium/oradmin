#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python Version: 2.6 - Platform: RedHat Enterprise Linux 5.10 64bits
# Created by Jonathan LAMBERT - contact@jonathanlambert.info

__author__ = "Jonathan LAMBERT"


import pygtk
pygtk.require('2.0')
import gtk


class Window:
	def __init__(self, titre, height="no", width="no"):
		self.fenetre=gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.fenetre.set_title(titre)
		self.color = gtk.gdk.color_parse('#CCCCCC')
		self.but_color = gtk.gdk.color_parse('#FFFFFF')
		self.fenetre.modify_bg(gtk.STATE_NORMAL, self.color)
		if height=="no" and width=="no":
			pass
		elif height=="max" and width=="max":
			self.fenetre.maximize()
		else:
			self.fenetre.set_default_size(width, height)
		self.fenetre.set_border_width(5)

	def error_dialog(self, msg):
		dialog = gtk.MessageDialog(
		parent         = None,
		flags          = gtk.DIALOG_MODAL,
		type           = gtk.MESSAGE_ERROR,
		buttons        = gtk.BUTTONS_OK,
		message_format = msg)
		dialog.set_title('Error !')
		dialog.connect('response', lambda dialog, response: dialog.destroy())
		color = gtk.gdk.color_parse('#DD5555')
		dialog.modify_bg(gtk.STATE_NORMAL, color)
		dialog.show()
		dialog.run()

	def warn_dialog(self, msg):
		dialog = gtk.MessageDialog(
		parent         = None,
		flags          = gtk.DIALOG_MODAL,
		type           = gtk.MESSAGE_WARNING,
		buttons        = gtk.BUTTONS_OK,
		message_format = msg)
		dialog.set_title('Warning')
		dialog.connect('response', lambda dialog, response: dialog.destroy())
		color = gtk.gdk.color_parse('#FFDD00')
		dialog.modify_bg(gtk.STATE_NORMAL, color)
		dialog.show()
		dialog.run()

	def notif_dialog(self, msg):
		dialog = gtk.MessageDialog(
		parent         = None,
		flags          = gtk.DIALOG_MODAL,
		type           = gtk.MESSAGE_INFO,
		buttons        = gtk.BUTTONS_OK,
		message_format = msg)
		dialog.set_title('Notification')
		dialog.connect('response', lambda dialog, response: dialog.destroy())
		color = gtk.gdk.color_parse('#FFFFFF')
		dialog.modify_bg(gtk.STATE_NORMAL, color)
		dialog.show()
		dialog.run()
