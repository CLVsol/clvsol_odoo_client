#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import argparse
import getpass
from functools import reduce


def secondsToStr(t):

    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class CLI(object):

    def __init__(
        self,
        server='http://localhost:8069',
        super_user_pw='super_user_pw',
        admin_user_pw='admin_user_pw',
        data_admin_user_pw='data_admin_user_pw',
        username='username',
        password='password',
        dbname='odoo',
        db_server='localhost',
        db_user='odoo',
        db_password='odoo',
        demo_data=False,
        upgrade_all=False,
        modules_to_upgrade=[],
        lang='pt_BR',
        tz='America/Sao_Paulo'

    ):

        self.server = server  # self.server = '*'
        self.super_user_pw = super_user_pw  # self.super_user_pw = '*'
        self.admin_user_pw = admin_user_pw  # self.super_user_pw = '*'
        self.data_admin_user_pw = data_admin_user_pw  # self.data_admin_user_pw = '*'
        self.username = username  # self.username = '*'
        self.password = password  # self.password = '*'
        self.dbname = dbname  # self.dbname = '*'
        self.db_server = db_server  # self.db_server = '*'
        self.db_user = db_user  # self.db_user = '*'
        self.db_password = db_password  # self.db_password = '*'
        self.demo_data = demo_data
        self.upgrade_all = upgrade_all
        self.modules_to_upgrade = modules_to_upgrade
        self.lang = lang
        self.tz = tz

    def argparse_db_setup(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('--server', action="store", dest="server")
        parser.add_argument('--super_user_pw', action="store", dest="super_user_pw")
        parser.add_argument('--admin_user_pw', action="store", dest="admin_user_pw")
        parser.add_argument('--data_admin_user_pw', action="store", dest="data_admin_user_pw")
        parser.add_argument('--db', action="store", dest="dbname")
        parser.add_argument('-d', '--demo_data', action='store_true', help='Install demo data')
        parser.add_argument('-a', '--upgrade_all', action='store_true', help='Upgrade all the modules')
        parser.add_argument('-m', '--modules', nargs='+', help='Modules to upgrade', required=False)
        parser.add_argument('--lang', action="store", dest="lang")
        parser.add_argument('--tz', action="store", dest="tz")

        args = parser.parse_args()
        # print('%s%s' % ('--> ', args))

        if args.server is not None:
            self.server = args.server
        elif self.server == '*':
            self.server = input('server: ')

        if args.super_user_pw is not None:
            self.super_user_pw = args.super_user_pw
        elif self.super_user_pw == '*':
            self.super_user_pw = getpass.getpass('super_user_pw: ')

        if args.admin_user_pw is not None:
            self.admin_user_pw = args.admin_user_pw
        elif self.admin_user_pw == '*':
            self.admin_user_pw = getpass.getpass('admin_user_pw: ')

        if args.data_admin_user_pw is not None:
            self.data_admin_user_pw = args.data_admin_user_pw
        elif self.data_admin_user_pw == '*':
            self.data_admin_user_pw = getpass.getpass('data_admin_user_pw: ')

        if args.dbname is not None:
            self.dbname = args.dbname
        elif self.dbname == '*':
            self.dbname = input('dbname: ')

        self.demo_data = args.demo_data

        self.upgrade_all = args.upgrade_all

        if args.modules is not None:
            self.modules_to_upgrade = args.modules

        if args.lang is not None:
            self.lang = args.lang

        if args.tz is not None:
            self.tz = args.tz

    def argparse_template(self):

        parser = argparse.ArgumentParser()
        parser.add_argument('--server', action="store", dest="server")
        parser.add_argument('--super_user_pw', action="store", dest="super_user_pw")
        parser.add_argument('--admin_user_pw', action="store", dest="admin_user_pw")
        parser.add_argument('--user', action="store", dest="username")
        parser.add_argument('--pw', action="store", dest="password")
        parser.add_argument('--db', action="store", dest="dbname")
        parser.add_argument('--dbserver', action="store", dest="db_server")
        parser.add_argument('--dbu', action="store", dest="db_user")
        parser.add_argument('--dbw', action="store", dest="db_password")

        args = parser.parse_args()
        # print('%s%s' % ('--> ', args))

        if args.server is not None:
            self.server = args.server
        elif self.server == '*':
            self.server = input('server: ')

        if args.super_user_pw is not None:
            self.super_user_pw = args.super_user_pw
        elif self.super_user_pw == '*':
            self.super_user_pw = getpass.getpass('super_user_pw: ')

        if args.admin_user_pw is not None:
            self.admin_user_pw = args.admin_user_pw
        elif self.admin_user_pw == '*':
            self.admin_user_pw = getpass.getpass('admin_user_pw: ')

        if args.dbname is not None:
            self.dbname = args.dbname
        elif self.dbname == '*':
            self.dbname = input('dbname: ')

        if args.username is not None:
            self.username = args.username
        elif self.username == '*':
            self.username = input('username: ')

        if args.password is not None:
            self.password = args.password
        elif self.password == '*':
            self.password = getpass.getpass('password: ')

        if args.db_server is not None:
            self.db_server = args.db_server
        elif self.db_server == '*':
            self.db_server = input('db_server: ')

        if args.db_user is not None:
            self.db_user = args.db_user
        elif self.db_user == '*':
            self.db_user = input('db_user: ')

        if args.db_password is not None:
            self.db_password = args.db_password
        elif self.db_password == '*':
            self.db_password = getpass.getpass('db_password: ')
