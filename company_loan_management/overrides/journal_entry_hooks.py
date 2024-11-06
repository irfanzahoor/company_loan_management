import frappe


def on_submit(doc, method=None):
	for d in doc.accounts:
		if d.reference_type != "Company Loan":
			continue

		if frappe.db.get_value("Account", d.account, "root_type") != "Liability":
			continue

		loan_doc = frappe.get_doc("Company Loan", d.reference_name)
		row = loan_doc.append("draws_and_repayments", {
			"date": doc.posting_date,
			"journal_entry": doc.name,
			"journal_entry_detail": d.name,
			"account": d.account,
			"debit": d.debit,
			"credit": d.credit,
		})

		row.insert()
		loan_doc.update_status(update=True)
		loan_doc.notify_update()


def on_cancel(doc, method=None):
	doc.ignore_linked_doctypes = (
		"GL Entry",
		"Stock Ledger Entry",
		"Payment Ledger Entry",
		"Repost Payment Ledger",
		"Repost Payment Ledger Items",
		"Repost Accounting Ledger",
		"Repost Accounting Ledger Items",
		"Unreconcile Payment",
		"Unreconcile Payment Entries",
		"Company Loan"
	)

	for d in doc.accounts:
		if d.reference_type != "Company Loan":
			continue

		loan_doc = frappe.get_doc("Company Loan", d.reference_name)

		row = None
		for loan_row in loan_doc.draws_and_repayments:
			if loan_row.journal_entry == doc.name and loan_row.journal_entry_detail == d.name:
				row = loan_row
				break

		if row:
			frappe.delete_doc(row.doctype, row.name)
			loan_doc = frappe.get_doc("Company Loan", d.reference_name)
			loan_doc.update_status(update=True)
			loan_doc.notify_update()
