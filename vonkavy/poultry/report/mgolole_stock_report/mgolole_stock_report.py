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
		
		row['item_code'] = d.item_code
		
		row['warehouse'] = d.warehouse
		row['actual_qty'] = d.actual_qty
		
		row['projected_qty'] = d.projected_qty
		
		row['stock_uom'] = d.stock_uom	


		data.append(row)

	return columns, data


def get_column():
	return [
		{
			"fieldname":"item_code",
			"label": "Item",
			"fieldtype": "Link",
			"options": "Item",
			"width": 150,
		},
		{
			"fieldname":"warehouse",
			"label": "Warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			'width': 200
		},		
		{
			"fieldname":"stock_uom",
			"label": "UOM",
			"fieldtype": "Link",
			"options": "UOM",
			'width': 120
		},
		{
			"fieldname":"actual_qty",
			"label": "Qty",
			"fieldtype": "Data",
			'width': 150
		},
		{
			"fieldname":"projected_qty",
			"label": "Projected",
			"fieldtype": "Data",
			'width': 150
		},

	
	]


def get_data(filters):
	where_filter = {"from_date": filters.from_date, "to_date": filters.to_date}
	where = ""


	data = frappe.db.sql("""select tb.item_code,
		tb.warehouse, tb.stock_uom, tb.actual_qty, tb.projected_qty
		
		from `tabBin` tb
		where tb.docstatus !=2 and 
		(tb.warehouse = "Mgolole store - VAC" or tb.warehouse = "Mgolole Mortality - VAC" )
		"""+ where, where_filter, as_dict=1)
	return data
