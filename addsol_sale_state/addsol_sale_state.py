from openerp.osv import fields, osv

class addsol_sale_state(osv.Model):

    _inherit = 'sale.order'
    
    
    def action_my_new_function(self, cr, uid, ids, context=None):
        res = self.write(cr, uid, ids, {'state': 'approve'}, context=context)    
        return res
    
    def trans_waitapproval(self, cr, uid, ids, context=None):
        res = self.write(cr, uid, ids, {'state': 'waitforapprove'}, context=context)    
        return res
    
    def check_for_approval(self, cr, uid, ids,context=None):
        flag= False
        sale_order = self.pool.get('sale.order')
        for order in sale_order.browse(cr, uid, ids, context):
            for order_line in order.order_line:
                if order_line.sale_price > order_line.price_unit:
                    flag = True
            print "check..................",order.credit, order.property_payment_term, order.payment_term, flag
            if order.credit != 0 or order.property_payment_term != order.payment_term or flag:
                return self.write(cr, uid, ids, {'state': 'waitforapprove'}, context=context)
            else:
                return self.write(cr, uid, ids, {'state': 'approve'}, context=context)
        
    
    _columns = {
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