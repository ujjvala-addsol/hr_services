from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp

class addsol_sale_type(osv.osv):
    _name = "sale.type"
    _description = "Sales Type"
    _columns = {
        'name':fields.char('Type', required=True, size=64),
        'prefix': fields.char('Prefix', required=True, size=16),
        'description': fields.text('Notes'),
    }

class addsol_sale_order(osv.osv):
    _inherit = "sale.order"
    _columns = {
        'po_no': fields.char('PO Number', size=64),
        'po_date': fields.date('PO Date'),
        'ref':fields.related('partner_id','ref',type='char',string='Customer Reference',size=64),
        'pan_no':fields.related('partner_id','pan_no',type='char',string='PAN No',size=64),
        'tin_no': fields.related('partner_id','tin_no',type='char',string='TIN No',size=64),
        'cst_no':fields.related('partner_id','cst_no',type='char',string='CST No',size=64),
        'excise_control_code':fields.related('partner_id','excise_no',type='char',string='Excise Control Code',size=64),
        'type_id':fields.many2one('sale.type' ,'Sales Type'),
        'credit':fields.related('partner_id','credit',type='float',string='Outstanding Balance'),
        'property_payment_term':fields.related('partner_id','property_payment_term',relation='account.payment.term',type='many2one',string='Payment Term'),
        'freight':fields.selection([('yes','YES'),('no','NO')],'Freight'),
        'state': fields.selection([
            ('draft', 'Draft Quotation'),
            ('waitforapprove','Waiting For Approval'),
            ('approve', 'Approved'),
            ('sent', 'Quotation Sent'),
            ('cancel', 'Cancelled'),
            ('waiting_date', 'Waiting Schedule'),
            ('progress', 'Sales Order'),
            ('manual', 'Sale to Invoice'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ], 'Status', readonly=True, track_visibility='onchange',
            help="Gives the status of the quotation or sales order. \nThe exception status is automatically set when a cancel operation occurs in the processing of a document linked to the sales order. \nThe 'Waiting Schedule' status is set when the invoice is confirmed but waiting for the scheduler to run on the order date.", select=True),
    }
    
    def create(self, cr, uid, vals, context=None):
        type_obj = self.pool.get('sale.type')
        seq_obj = self.pool.get('ir.sequence')
        seq_ids = seq_obj.search(cr, uid, [('code','=','sale.order')], context=context)
        if vals.get('name','/')=='/':
            if vals.get('type_id'):
                sale_type = type_obj.browse(cr, uid, vals.get('type_id'), context=context).prefix
                seq_obj.write(cr, uid, seq_ids, {'prefix': sale_type}, context=context)
            else:
                seq_obj.write(cr, uid, seq_ids, {'prefix': 'SO'}, context=context)
            vals['name'] = seq_obj.get(cr, uid, 'sale.order') or '/'
        return super(addsol_sale_order, self).create(cr, uid, vals, context=context)
    
    def action_my_new_function(self, cr, uid, ids, context=None):
        res = self.write(cr, uid, ids, {'state': 'approve'}, context=context)
        return res
    
    def check_for_approval(self, cr, uid, ids,context=None):
        flag= False
        sale_order = self.pool.get('sale.order')
        for order in sale_order.browse(cr, uid, ids, context):
            for order_line in order.order_line:
                if order_line.sale_price > order_line.price_unit:
                    flag = True
            if order.credit != 0 or order.property_payment_term != order.payment_term or flag:
                return self.write(cr, uid, ids, {'state': 'waitforapprove'}, context=context)
            else:
                return self.write(cr, uid, ids, {'state': 'approve'}, context=context)
    
class addsol_sale_order_line(osv.osv):
    
    _inherit = "sale.order.line"
    _columns = {
        'detail': fields.char('Detail',size=64),
        'sale_price':fields.float('sale price',digits_compute= dp.get_precision('Product Price'))
    }

    def product_id_change(self, cr, uid, ids, pricelist, product,qty=0,uom=False, qty_uos=0, uos=False, name='', partner_id=False,lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        value =  super(addsol_sale_order_line, self).product_id_change(cr, uid, ids, pricelist,product, qty, uom, qty_uos,uos, name, partner_id, lang,update_tax, date_order, packaging=packaging,fiscal_position=fiscal_position,flag=flag, context=context)
        if not product:
            return {'value': {'sale_price': 0.0}}
        prod = self.pool.get('product.template').browse(cr, uid, product, context=context)
        sale_price = prod.list_price or 0.0
        value['value'].update({'sale_price': sale_price})
        return value

