# Copyright (c) 2024, git529 and contributors
# For license information, please see license.txt

# import frappe
from frappe.utils import flt, getdate
from frappe.model.document import Document


class CompanyLoan(Document):
	def validate(self):
		self.update_status()

	def update_status(self, update=False, update_modified=True):
		self.outstanding_balance = 0

		if self.draws_and_repayments:
			self.draws_and_repayments.sort(key=lambda d: getdate(d.date))

			for idx, d in enumerate(self.draws_and_repayments or []):
				self.outstanding_balance += flt(d.credit)
				self.outstanding_balance -= flt(d.debit)
				d.balance = self.outstanding_balance
				d.idx = idx + 1

				if update:
					d.db_set({
						'idx': d.idx,
						'balance': d.balance,
					}, update_modified=update_modified)

		if self.docstatus == 0:
			self.status = "Draft"
		elif not len(self.draws_and_repayments or []):
			self.status = "Draft"
		elif flt(self.outstanding_balance) > 0:
			self.status = "Outstanding"
		elif flt(self.outstanding_balance) == 0:
			self.status = "Paid Off"
		else:
			self.status = "Overpaid"

		if update:
			self.db_set({
				'outstanding_balance': self.outstanding_balance,
				'status': self.status,
			}, update_modified=update_modified)
