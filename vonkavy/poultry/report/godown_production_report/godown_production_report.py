# Copyright (c) 2022, KODEIT and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_column()
	data=[]

	report_items = get_data(filters)
	for d in report_items:
		row = {}
		
		row['item_code'] = d.production_item
		
		row['name'] = d.name
		row['produced_qty'] = d.produced_qty
		if row['produced_qty']:
			row['bag_qty'] = (row['produced_qty'] / 50)
		
		row['creation'] = d.creation
		
		row['stock_uom'] = d.stock_uom	


		data.append(row)

	return columns, data


def get_column():
	return [
		{
			"fieldname":"creation",
			"label": "Date",
			"fieldtype": "Date",
			'width': 150
		},
		{
			"fieldname":"item_code",
			"label": "Item",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150,
		},
		{
			"fieldname":"produced_qty",
			"label": "Qty (kg)",
			"fieldtype": "Data",
			'width': 150
		},
		{
			"fieldname":"bag_qty",
			"label": "Qty (Bags)",
			"fieldtype": "Data",
			'width': 150
		},
		{
			"fieldname":"name",
			"label": "Work Order",
			"fieldtype": "Link",
			"options": "Work Order",
			'width': 200
		},		
		

	
	]


def get_data(filters):
	where_filter = {"from_date": filters.from_date, "to_date": filters.to_date}
	where = ""


	data = frappe.db.sql("""select two.production_item,
		two.name, two.produced_qty, two.creation
		
		from `tabWork Order` two
		where two.creation BETWEEN %(from_date)s AND %(to_date)s  
		AND two.docstatus =1 AND two.status = 'Completed'		
		"""+ where, where_filter, as_dict=1)
	return data
