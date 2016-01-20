#! /usr/bin/python
# Python Version: 2.7 - Platform: RedHat Enterprise Linux 5.10 64bits
# Created by Jonathan LAMBERT - jlambert@sigma.fr - www.sigma.fr

__author__ = "Jonathan LAMBERT"

import Database

class OraTool(Database.Oracle):

        def __init__(self, base, user="", password=""):
                Database.Oracle.__init__(self, user, password, base)
                self.user = user
                self.password = password
                self.base = base

