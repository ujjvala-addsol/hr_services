# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
  'name': 'Addsol Sales Order ',
  'version': '1.0',
  'author': 'Addition IT Solutions Pvt. Ltd.',
  'category': 'Sales',
  'description': """
Addition IT Solutions Pvt. Ltd.
====================================
Contact :
    * website : www.aitspl.com
    * email   : info@aitspl.com

Sales Order module:
--------------------------------------------
    * Add 'Currency Rate' field in Supplier Invoice
    * Add 'Supplier Unit Price' field in Invoice line
    * On Change of 'Supplier Unit Price', a multiplication of 'Currency Rate' and 
    'Supplier Unit Price' is written to 'Unit Price' field.

The processes is for import bills in different currencies.
    """,
  'website': 'http://www.aitspl.com',
  'images' : ['images/addsol.png'],
  'depends': ['addsol_sale_code','sale'],
  'data': ['addsol_sale_order.xml'],
  'demo': [],
  'installable': True,
}