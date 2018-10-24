# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import erppeek  # http://erppeek.readthedocs.io/en/1.6.2/api.html#manage-addons
import xmlrpc.client as xmlrpclib


class DB(object):

    def __init__(
        self,
        server='http://localhost:8069',
        super_user_pw='super_user_pw',
        admin_user_pw='admin_user_pw',
        data_admin_user_pw='data_admin_user_pw',
        dbname='odoo',
        demo_data=False,
        upgrade_all=False,
        modules_to_upgrade=[],
        lang='pt_BR',
        tz='America/Sao_Paulo'
    ):

        self.server = server
        self.super_user_pw = super_user_pw
        self.admin_user_pw = admin_user_pw
        self.data_admin_user_pw = data_admin_user_pw
        self.dbname = dbname
        self.demo_data = demo_data
        self.upgrade_all = upgrade_all
        self.modules_to_upgrade = modules_to_upgrade
        self.lang = lang
        self.tz = tz

    def create(self):

        sock_common = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/2/common')
        print('sock_common.version(): "{0}"'.format(sock_common.version()))
        uid = sock_common.login(self.dbname, 'admin', self.admin_user_pw)
        print('uid: "{0}"'.format(uid))

        client = erppeek.Client(server=self.server)
        print('Databases found: {0}'.format(client.db.list()))

        if self.dbname not in client.db.list():

            print('Creating database "{0}"...'.format(self.dbname))

            client.create_database(
                passwd=self.super_user_pw,
                database=self.dbname,
                demo=self.demo_data,
                lang=self.lang,
                user_password=self.admin_user_pw
            )

            print('Done.')
            return True

        else:

            print('Database "{0}" already exists.'.format(self.dbname))
            print('Done.')
            return False

    def my_company_setup(self, CompanyName, website, Company_image):

        print('Configuring My Company...')

        client = erppeek.Client(
            server=self.server,
            db=self.dbname,
            user='admin',
            password=self.admin_user_pw)

        ResPartner = client.model('res.partner')
        args = [('name', '=', 'My Company'), ]
        partner_id = ResPartner.browse(args).id

        if partner_id != []:

            values = {
                'name': CompanyName,
                'email': '',
                'website': website,
                'tz': self.tz,
                'lang': self.lang,
                'image': Company_image,
            }
            ResPartner.write(partner_id, values)

            ResCompany = client.model('res.company')
            args = [('name', '=', 'My Company'), ]
            company_id = ResCompany.browse(args).id

            values = {
                'name': CompanyName,
                'email': '',
                'website': website,
                'logo': Company_image,
            }
            ResCompany.write(company_id, values)

            print('Done.')

        else:

            print('"{0}" already configured.'.format(self.dbname))
            print('Done.')

    def administrator_setup(self, admin_user_email, Administrator_image):

        print('Configuring user "Administrator"...')

        client = erppeek.Client(
            server=self.server,
            db=self.dbname,
            user='admin',
            password=self.admin_user_pw)

        ResUsers = client.model('res.users')
        args = [('name', '=', 'Administrator'), ]
        user = ResUsers.browse(args)

        if user[0].email != admin_user_email:

            values = {
                'lang': self.lang,
                'tz': self.tz,
                'email': admin_user_email,
                'image': Administrator_image,
            }
            ResUsers.write(user.id, values)

            group_name_list = [
                'Contact Creation',
            ]
            self.user_groups_setup('Administrator', group_name_list)

            print('Done.')

        else:

            print('User "{0}" already configured.'.format(user.name))
            print('Done.')

    def demo_user_setup(self, demo_user_name, demo_user_email, CompanyName, demo_user, demo_user_pw, Demo_User_image):

        print('Configuring user "Demo"...')

        client = erppeek.Client(
            server=self.server,
            db=self.dbname,
            user='admin',
            password=self.admin_user_pw)

        ResUsers = client.model('res.users')
        args = [('name', '=', demo_user_name), ]
        user = ResUsers.browse(args)

        if user.id == []:

            ResPartner = client.model('res.partner')
            args = [('name', '=', CompanyName), ]
            parent_id = ResPartner.browse(args).id

            ResCompany = client.model('res.company')
            args = [('name', '=', CompanyName), ]
            company_id = ResCompany.browse(args).id

            values = {
                'name': demo_user_name,
                'customer': False,
                'employee': False,
                'is_company': False,
                'email': demo_user_email,
                'website': '',
                'parent_id': parent_id[0],
                'company_id': company_id[0],
                'tz': self.tz,
                'lang': self.lang
            }
            partner_id = ResPartner.create(values)

            values = {
                'name': demo_user_name,
                'partner_id': partner_id,
                'company_id': company_id[0],
                'login': demo_user,
                'password': demo_user_pw,
                'image': Demo_User_image,
            }
            ResUsers.create(values)

            print('Done.')

        else:

            print('User "{0}" already configured.'.format(demo_user_name))
            print('Done.')

    def data_administrator_user_setup(
        self, data_admin_user_name, data_admin_user_email, CompanyName,
        data_admin_user, data_admin_user_pw, DataAdministrator_image
    ):

        print('Configuring user "Data Administrator"...')

        client = erppeek.Client(
            server=self.server,
            db=self.dbname,
            user='admin',
            password=self.admin_user_pw)

        ResUsers = client.model('res.users')
        args = [('name', '=', data_admin_user_name), ]
        user = ResUsers.browse(args)

        if user.id == []:

            ResPartner = client.model('res.partner')
            args = [('name', '=', CompanyName), ]
            parent_id = ResPartner.browse(args).id

            ResCompany = client.model('res.company')
            args = [('name', '=', CompanyName), ]
            company_id = ResCompany.browse(args).id

            values = {
                'name': data_admin_user_name,
                'customer': False,
                'employee': False,
                'is_company': False,
                'email': data_admin_user_email,
                'website': '',
                'parent_id': parent_id[0],
                'company_id': company_id[0],
                'tz': self.tz,
                'lang': self.lang
            }
            partner_id = ResPartner.create(values)

            values = {
                'name': data_admin_user_name,
                'partner_id': partner_id,
                'company_id': company_id[0],
                'login': data_admin_user,
                'password': data_admin_user_pw,
                'image': DataAdministrator_image,
            }
            ResUsers.create(values)

            print('Done.')

        else:

            print('User "{0}" already configured.'.format(data_admin_user_name))
            print('Done.')

    def user_groups_setup(self, user_name, group_name_list):

        print('Executing user_groups_setup...')

        client = erppeek.Client(
            server=self.server,
            db=self.dbname,
            user='admin',
            password=self.admin_user_pw)

        ResUsers = client.model('res.users')
        args = [('name', '=', user_name), ]
        user_id = ResUsers.browse(args).id

        ResGroups = client.model('res.groups')

        for group_name in group_name_list:
            args = [('name', '=', group_name)]
            group_id = ResGroups.browse(args).id
            values = {
                'groups_id': [(4, group_id[0])],
            }
            ResUsers.write(user_id, values)

        print('Done.')

    def module_install_upgrade(self, module_name, upgrade=False):

        print('Module Name: "{0}" (Update: {1})'.format(module_name, upgrade))

        client = erppeek.Client(
            server=self.server,
            db=self.dbname,
            user='admin',
            password=self.admin_user_pw)

        modules = client.modules()
        if module_name in modules['uninstalled']:
            print('Installing module "{0}"...'.format(module_name))
            client.install(module_name)
            print('Done.')
            return True

        elif upgrade:
            print('Upgrading module "{0}"...'.format(module_name))
            client.upgrade(module_name)
            print('Done.')
            return True

        else:
            print('Skipping module "{0}"...'.format(module_name))
            print('Done.')
            return False

