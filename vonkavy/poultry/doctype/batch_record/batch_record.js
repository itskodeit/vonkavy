// Copyright (c) 2022, KODEIT and contributors
// For license information, please see license.txt


frappe.ui.form.on('Batch Record', {
	refresh: function(frm) {

	},

	batch_date: function(frm) {
		var aday = new Date();
		var to_date = aday.toISOString().split('T')[0];
		var days = frappe.datetime.get_diff(to_date,frm.doc.batch_date) ;
		var weekNumber = Math.ceil(days / 7);
		
		frm.set_value("week", weekNumber);

		refresh_field(frm.doc.week);
		console.log(weekNumber);
		console.log(frappe.datetime.get_diff(to_date,frm.doc.batch_date))
	},
});
