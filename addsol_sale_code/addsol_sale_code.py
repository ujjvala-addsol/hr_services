from openerp.osv import fields, osv

class addsol_sale_code(osv.Model):
	_name = "sale.code"
	_description = "Sales Code"
	_columns = {
			'code':fields.char('Sale Code',size=8),
			'name':fields.char('Sale Code Name',size=28),
			'description':fields.char('Description',size=256),
			'sequence_id':fields.many2one('ir.sequence.type','sequence code')
	}
			

