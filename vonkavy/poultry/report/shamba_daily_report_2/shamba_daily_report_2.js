// Copyright (c) 2022, KODEIT and contributors
// For license information, please see license.txt
/* eslint-disable */
var aday = new Date();
var to_date = aday.toISOString().split('T')[0];
aday.setDate(aday.getDate() - 7);
var from_date = aday.toISOString().split('T')[0];
var cur_report = null;


frappe.query_reports["Shamba Daily Report 2"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": from_date,
			"width": "80"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": to_date
		},
		{
			"fieldname":"batch_ref",
			"label": __("Batch"),
			"fieldtype": "Link",
			"options": "Batch",
			"width": "80"
		},
	]
};
