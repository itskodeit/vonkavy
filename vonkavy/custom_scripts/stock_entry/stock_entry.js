erpnext.stock.StockEntry = erpnext.stock.StockEntry.extend({
	onload: function(frm){

	},
	batch: function(doc) {
		this.set_warehouse_in_children(doc.items, "batch_no", doc.batch);
	},
	/*batch: function(frm) {
		$.each(child_table || [], function(i, item) {
				frappe.model.set_value(doctype, item.name, warehouse_field, warehouse);
			});
		
		frm.set_value("week", weekNumber);

		refresh_field(frm.doc.week);
		console.log(weekNumber);
		console.log(frappe.datetime.get_diff(to_date,frm.doc.manufacturing_date))
	},*/
});

$.extend(cur_frm.cscript, new erpnext.stock.StockEntry({frm: cur_frm}));