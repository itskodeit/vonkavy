# Copyright (c) 2022, KODEIT and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
	if not filters:
		filters = {}

	columns = get_column()
	data=[]

	report_items = get_data(filters)
	#frappe.throw(frappe.as_json(report_items))
	for d in report_items:
		row = {}
		
		row['date'] = d.posting_date
		row['name'] = d.name
		row['batch_ref'] = d.batch

		row["eggs"] = get_egg_qty(d.posting_date, d.batch, "Mayai", "Dakawa store - VAC") or 0
		row["breakage"] = get_egg_qty(d.posting_date, d.batch, "Mayai", "Dakawa Breakage - VAC") or 0
		row["total_eggs"] = row["eggs"] + row["breakage"]

		# kuku_var section to ignore
		kuku_var = get_kuku_qty(d.posting_date, d.batch, "Kuku", "Dakawa store - VAC") or 0
		if kuku_var !=0:
			row["kuku_stock"] = kuku_var
		else:
			row["kuku_stock"] = get_kuku("Kuku", "Dakawa store - VAC")
		
		# end of kuku_var

		row["mortality"] = get_kuku_qty(d.posting_date, d.batch, "Kuku", "Dakawa Mortality - VAC") or 0

		row["kuku_sold"] = get_kuku_sold(d.posting_date, d.batch,"Kuku", "Dakawa store - VAC", "Sales Invoice") or 0
		row["kuku_by_batch"] = get_kuku_batch(d.posting_date, d.batch,"Kuku", "Dakawa store - VAC") or 0 

		if row["total_eggs"] !=0:
			row["percent"] = (row["eggs"] / row["total_eggs"] ) * 100
		else:
			row["percent"] = 0

		row["feeds"] = get_consumed_qty(d.posting_date, d.batch, "Growers Mash", "Dakawa store - VAC") or 0
		row["vaccine"] = get_consumed_qty(d.posting_date, d.batch, "Vaccine", "Dakawa store - VAC") or 0
		row["water"] = get_consumed_qty(d.posting_date, d.batch, "Water", "Dakawa store - VAC") or 0
	
		# if d.posting_date == row['date'] and d.batch == row["batch_ref"]:
			
		# 	if d.item_code == "Mayai":
		# 		if d.t_warehouse == "Breakage Warehouse - Vk":
		# 			row['breakage'] = d.qty
		# 		else:
		# 			row['eggs'] = d.qty
		# 	#row['total_eggs'] = row["eggs"] + row["breakage"]

			# if d.item_code == "Kuku":
			# 	if d.t_warehouse == "Mortality Warehouse - Vk":
			# 		row['mortality'] = d.qty
			# 	else:
			# 		row['kuku_stock'] = d.qty

		row['item_code'] = d.item_code
		row['qty'] = d.qty
		row['t_warehouse'] = d.t_warehouse
		
		# row['last_updated_on'] = d.modified
		# row['kiasi'] = d.kiasi
		# row['balance'] = d.balance	


		data.append(row)
		#frappe.throw(frappe.as_json(data))

	return columns, data


def get_column():
	return [
		# {
		# 	"fieldname":"name",
		# 	"label": "Reference",
		# 	"fieldtype": "Link",
		# 	"options": "Stock Entry",
		# 	"width": 120,
		# },
		{
			"fieldname":"batch_ref",
			"label": "Batch",
			"fieldtype": "Data",
			'width': 150
		},
		{
			"fieldname":"date",
			"label": "Tarehe",
			"fieldtype": "Date",
			'width': 150
		},
		{
			"fieldname":"eggs",
			"label": "Eggs",
			"fieldtype": "Data",
			'width': 120
		},
		{
			"fieldname":"breakage",
			"label": "Breakage",
			"fieldtype": "Data",
			'width': 120
		},
		{
			"fieldname":"total_eggs",
			"label": "Total",
			"fieldtype": "Data",
			'width': 120
		},
		{
			"fieldname":"percent",
			"label": "Percent",
			"fieldtype": "Float",
			'width': 120
		},
		{
			"fieldname":"mortality",
			"label": "Mortality",
			"fieldtype": "Data",
			"width": 120,
		},
		# {
		# 	"fieldname":"kuku_stock",
		# 	"label": "Stock",
		# 	"fieldtype": "Data",
		# 	'width': 120
		# },
		# {
		# 	"fieldname":"kuku_sold",
		# 	"label": "Sold",
		# 	"fieldtype": "Data",
		# 	'width': 120
		# },
		{
			"fieldname":"kuku_by_batch",
			"label": "Stock By Batch",
			"fieldtype": "Data",
			'width': 120
		},
		{
			"fieldname":"qty",
			"label": "Weight",
			"fieldtype": "Float",
			'width': 120
		},
		{
			"fieldname":"feeds",
			"label": "Feeds",
			"fieldtype": "Data",
			'width': 120
		},
		
		{
			"fieldname":"water",
			"label": "Water Vol",
			"fieldtype": "Float",
			'width': 120
		},
		{
			"fieldname":"vaccine",
			"label": "Vaccine",
			"fieldtype": "Data",
			'width': 150
		},		

	
	]


def get_data(filters):
	where_filter = {"from_date": filters.from_date, "to_date": filters.to_date}
	where = ""

	data = frappe.db.sql("""select tse.name, tse.batch,
		tse.posting_date, tse.purpose, tsd.item_code, tsd.qty, tsd.s_warehouse,
		tsd.t_warehouse, tsd.s_warehouse
		
		from `tabStock Entry Detail` tsd
		LEFT JOIN
			`tabStock Entry` tse ON tsd.parent = tse.name
		LEFT JOIN
			`tabBatch Record` tbr ON tse.batch = tbr.name
		where tse.posting_date BETWEEN %(from_date)s AND %(to_date)s
		AND tse.batch != '' AND tse.docstatus !=2
		GROUP BY tse.posting_date, tse.batch
		order by tse.posting_date ASC
		"""+ where, where_filter, as_dict=1)
	return data


def get_egg_qty(date, batch, item, warehouse):
	qty = 0
	data= frappe.db.sql("""select ed.qty, ed.s_warehouse, ed.t_warehouse, 
		se.posting_date, se.batch  
		from `tabStock Entry` se
		inner join
		`tabStock Entry Detail` ed on se.name = ed.parent
		where posting_date = %s and batch = %s and item_code = %s and t_warehouse=%s
		""",(date, batch, item,warehouse))
	if data:
		qty = data[0][0] or 0
	return qty

def get_kuku_qty(date, batch, item, warehouse):
	qty = 0
	data= frappe.db.sql("""select ed.qty, ed.s_warehouse, ed.t_warehouse, 
		se.posting_date, se.batch 
		from `tabStock Entry` se
		inner join
		`tabStock Entry Detail` ed on se.name = ed.parent
		where posting_date = %s and batch = %s and item_code = %s and t_warehouse=%s
		""",(date, batch, item,warehouse))
	if data:
		qty = data[0][0] or 0
	return qty

def get_kuku(item, warehouse):
	qty = 0
	data= frappe.db.sql("""select actual_qty-reserved_qty from `tabBin`
		where item_code = %s and warehouse=%s
		""",(item,warehouse))
	if data:
		qty = data[0][0] or 0
	return qty

def get_consumed_qty(date, batch, item, warehouse):
	qty = 0
	data= frappe.db.sql("""select ed.qty, ed.s_warehouse, ed.t_warehouse, 
		se.posting_date, se.batch 
		from `tabStock Entry` se
		inner join
		`tabStock Entry Detail` ed on se.name = ed.parent
		where posting_date = %s and batch = %s and item_code = %s and s_warehouse=%s
		""",(date, batch, item,warehouse))
	if data:
		qty = data[0][0] or 0
	return qty

# def get_total_sold(item):
# 	data= frappe.db.sql("""select p.posting_date, c.qty from `tabSales Invoice` p inner join 
# 		`tabSales Invoice Item` c on p.name = c.parent where c.item_code = %s and p.docstatus = 1
# 		""",(item), as_dict=1)
# 	return data


def get_kuku_batch(date, batch, item, warehouse):
	qty = 0
	data= frappe.db.sql("""select sum(sle.actual_qty), sle.warehouse, sle.item_code, 
		sle.posting_date, sle.batch_no 
		from `tabStock Ledger Entry` sle
		where posting_date <= %s and batch_no = %s and item_code = %s and warehouse=%s
		and sle.docstatus != 2
		""",(date, batch, item,warehouse))
	if data:
		qty = data[0][0] or 0
	return qty

def get_kuku_sold(date, batch, item, warehouse, voucher_type):
	qty = 0
	data= frappe.db.sql("""select sum(sle.actual_qty), sle.warehouse, sle.item_code, 
		sle.posting_date, sle.batch_no, sle.voucher_type
		from `tabStock Ledger Entry` sle
		where posting_date = %s and batch_no = %s and item_code = %s and warehouse=%s
		and sle.docstatus != 2 and voucher_type = %s
		""",(date, batch, item,warehouse, voucher_type))
	if data:
		qty = data[0][0] or 0
	return qty