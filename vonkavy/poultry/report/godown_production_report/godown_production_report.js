// Copyright (c) 2022, KODEIT and contributors
// For license information, please see license.txt
/* eslint-disable */
var aday = new Date();
aday.setDate(aday.getDate() + 1);
var to_date = aday.toISOString().split('T')[0];

var fday = new Date();
fday.setDate(aday.getDate() - 7);
var from_date = fday.toISOString().split('T')[0];
var cur_report = null;


frappe.query_reports["Godown Production Report"] = {
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
		/*{
			"fieldname":"warehouse",
			"label": __("Warehouse"),
			"fieldtype": "Link",
			"options": "Warehouse",
			"default": "Godown Store - VAC",
		},*/
	]
};
