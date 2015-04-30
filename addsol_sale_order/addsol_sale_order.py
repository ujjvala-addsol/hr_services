from openerp.osv import fields, osv
from openerp import netsvc
import time
import openerp.addons.decimal_precision as dp

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
        'code_id':fields.many2one('sale.code' ,'code'),
        'credit':fields.related('partner_id','credit',type='float',string='Outstanding Balance'),
        'property_payment_term':fields.related('partner_id','property_payment_term',relation='account.payment.term',type='many2one',string='Payment Term'),
        'freight':fields.selection([('yes','YES'),('no','NO')],'Freight')
        
    }
    
       
    
    
class addsol_sale_order_line(osv.osv):
    
    _inherit = "sale.order.line"
    
    _columns = {
        'detail': fields.char('Detail',size=64),
        'sale_price':fields.float('sale price',digits_compute= dp.get_precision('Product Price'))
    }
    
        
    def product_id_change(self, cr, uid, ids, pricelist, product,qty=0,uom=False, qty_uos=0, uos=False, name='', partner_id=False,lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        value =  super(addsol_sale_order_line, self).product_id_change(cr, uid, ids, pricelist,product, qty, uom, qty_uos,uos, name, partner_id, lang,update_tax, date_order, packaging=packaging,fiscal_position=fiscal_position,flag=flag, context=context)
        if not product:
            return {'value': {'sale_price': False}}
            
        prod = self.pool.get('product.template').browse(cr, uid, product, context=context)
        sale_price = prod.list_price or 0.0
        print "\n\n\n======= price ==========", sale_price
        # val ={
             # 'sale_price': sale_price,
            # }
        val= value['value']
        val.update({
             'sale_price': sale_price,
            })
        value.update({'value':val})
        print "\n\n\n======= value ==========",value
        return value
       
    

    