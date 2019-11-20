# Copyright (c) 2013, Officexlr Business Solutions Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	data = prepare_data(filters)
	columns = get_columns(filters)

	return columns, data

def get_columns(filters=None):
	return [
		{
			"label": "Sales Order Number",
			"fieldtype": "Link",
			"fieldname": "sales_order_no",
			"options":"Sales Order"
			
		},
		{
			"label": "Sales Order Value",
			"fieldtype": "Data",
			"fieldname": "sales_order_value",
		
		},
		{
			"label": "Budget",
			"fieldtype": "Data",
			"fieldname": "budget",
			
		},
		{
			"label": "Ordered",
			"fieldtype": "Data",
			"fieldname": "ordered",
			
		},
		{
			"label": "Balanced Ordering",
			"fieldtype": "Data",
			"fieldname": "balance_ordering",
			
		},
		{
			"label": "Cost Booked",
			"fieldtype": "Data",
			"fieldname": "cost_booked",
		
		},
		{
			"label": "Yet To Receive",
			"fieldtype": "Data",
			"fieldname": "yet_to_receive",
			
		},
		{
			"label": "Cost To Completion",
			"fieldtype": "Data",
			"fieldname": "cost_to_completion",
			
		},
		{
			"label": "Payment Made",
			"fieldtype": "Data",
			"fieldname": "payment_made",
	
		},
		{
			"label": "Payment To Made",
			"fieldtype": "Data",
			"fieldname": "payment_to_made",
		
		},
		{
			"label": "Sales Invoice",
			"fieldtype": "Data",
			"fieldname": "sales_invoice",
			
		},
		{
			"label": "Balance Invoice",
			"fieldtype": "Data",
			"fieldname": "balance_invoice",
			
		},
		{
			"label": "Contribution",
			"fieldtype": "Data",
			"fieldname": "contribution",
			
		},
		{
			"label": "Projected Final Contribution",
			"fieldtype": "Data",
			"fieldname": "projected_final_contribution",
			
		},

	]

def prepare_data(filters):
	sales_list = frappe.db.sql("""select 
		name,base_grand_total
		FROM `tabSales Order`;""", as_dict= True)
	
	data=[]
	for sa in sales_list:
		budget_list= frappe.db.sql("""select budget_b from `tabSales Order Item` where parent='{0}';""".format(sa.name),as_dict=True)
		budget=0
		ord_amount=0
		pi_grand_amount=0
		payment_made=0
		si_grand_amount=0
		for bd in budget_list:
				if bd.budget_b:
				budget+=bd.budget_b
		sales_invoice_list=frappe.db.sql("""select distinct(parent) from `tabSales Invoice Item` where sales_order='{0}';""".format(sa.name),as_dict=True)
		po_item_list= frappe.db.sql("""select distinct(parent) from `tabPurchase Order Item` where sales_order='{0}';""".format(sa.name),as_dict=True)
		for po_item in po_item_list:
			po_grand=frappe.db.sql("""select grand_total from `tabPurchase Order` where name='{0}';""".format(po_item.parent),as_dict=True)
			pi_item_list=frappe.db.sql("""select distinct(parent) from `tabPurchase Invoice Item` where purchase_order='{0}';""".format(po_item.parent),as_dict=True)
			for grand in po_grand:
				ord_amount+=grand.grand_total
			for pi_parent in pi_item_list:
				po_grand=frappe.db.sql("""select grand_total from `tabPurchase Invoice` where name='{0}';""".format(pi_parent.parent),as_dict=True)
				payment_list=frappe.db.sql("""select allocated_amount from `tabPayment Entry Reference` where reference_name='{0}';""".format(pi_parent.parent),as_dict=True)
				for pi_grand in po_grand:
					pi_grand_amount+=pi_grand.grand_total
				for payment in payment_list:
					payment_made +=payment.allocated_amount
		for si_data in sales_invoice_list:
			si_grand=frappe.db.sql("""select base_grand_total from `tabSales Invoice` where name='{0}';""".format(si_data.parent),as_dict=True)
			for si_total in si_grand:
				si_grand_amount+=si_total.base_grand_total
		prow = {
			"sales_order_no":sa.name,
			"sales_order_value":sa.base_grand_total,
			"budget":budget,
			"ordered":ord_amount,
			"balance_ordering":sa.base_grand_total-ord_amount,
			"cost_booked":pi_grand_amount,
			"yet_to_receive":ord_amount-pi_grand_amount,
			"cost_to_completion":(sa.base_grand_total-ord_amount)-(ord_amount-pi_grand_amount),
			"payment_made":payment_made,
			"payment_to_made":pi_grand_amount-payment_made,
			"sales_invoice":si_grand_amount,
			"balance_invoice":sa.base_grand_total-si_grand_amount,
			"contribution":(sa.base_grand_total-ord_amount)/sa.base_grand_total,
			"projected_final_contribution":(sa.base_grand_total-(ord_amount+sa.base_grand_total-ord_amount))/sa.base_grand_total

		}	
		data.append(prow)
	return data