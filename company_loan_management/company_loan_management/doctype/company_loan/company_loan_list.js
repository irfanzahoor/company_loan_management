
frappe.listview_settings["Company Loan"] = {
	add_fields: [
		"status",
	],
	get_indicator: function (doc) {
        if (doc.status == "Draft") {
            return [__(doc.status), "red", 1];
        } else if (doc.status == "Outstanding") {
            return [__(doc.status), "purple", 1];
        } else if (doc.status == "Paid Off") {
            return [__(doc.status), "green", 1];
        } else if (doc.status == "Overpaid") {
            return [__(doc.status), "orange", 1];            
        }
 
	},
};
