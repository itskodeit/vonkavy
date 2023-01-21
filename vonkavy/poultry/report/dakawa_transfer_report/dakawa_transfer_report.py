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
		
		row['posting_date'] = d.posting_date
		row['item_code'] = d.item_code
		
		row['s_warehouse'] = d.s_warehouse
		row['t_warehouse'] = d.t_warehouse
		row['actual_qty'] = d.qty
		
		row['driver_name'] = d.driver_name
		row['vehicle_no'] = d.vehicle_no
		
		row['stock_uom'] = d.uom
		row['transfer_no'] = d.name	


		data.append(row)

	return columns, data


def get_column():
	return [
		{
			"fieldname":"posting_date",
			"label": "Tarehe",
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
			"fieldname":"s_warehouse",
			"label": "Source",
			"fieldtype": "Link",
			"options": "Warehouse",
			'width': 200
		},
		{
			"fieldname":"t_warehouse",
			"label": "Destination",
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
			"fieldname":"driver_name",
			"label": "Driver",
			"fieldtype": "Data",
			'width': 150
		},
		{
			"fieldname":"vehicle_no",
			"label": "Vehicle No",
			"fieldtype": "Data",
			'width': 150
		},
		{
			"fieldname":"transfer_no",
			"label": "Transfer",
			"fieldtype": "Link",
			"options": "Stock Entry",
			'width': 120
		},

	
	]


def get_data(filters):
	where_filter = {"from_date": filters.from_date, "to_date": filters.to_date}
	where = ""


	data = frappe.db.sql("""select tse.name, tse.batch,
		tse.posting_date, tse.purpose, tse.driver_name, tse.vehicle_no,
		tsd.item_code, tsd.qty, tsd.s_warehouse,
		tsd.t_warehouse, tsd.s_warehouse, tsd.uom
		
		from `tabStock Entry Detail` tsd
		LEFT JOIN
			`tabStock Entry` tse ON tsd.parent = tse.name
		where tse.posting_date BETWEEN %(from_date)s AND %(to_date)s
		AND tse.purpose = 'Material Transfer' AND tse.docstatus !=2
		AND (tsd.s_warehouse = 'Dakawa store - VAC' or tsd.t_warehouse ='Dakawa store - VAC')
		AND (tsd.t_warehouse != 'Dakawa Breakage - VAC' and tsd.t_warehouse !='Dakawa Mortality - VAC')
		GROUP BY tse.posting_date
		order by tse.posting_date ASC
		"""+ where, where_filter, as_dict=1)
	return data
