# Copyright (c) 2024, techbirdit and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Boiling(Document):
    def before_save(self):
        if self.weight and not self.balance:
            # Fetch the current total quantity for the selected value
            # total_quantity = frappe.db.get_value(
            #     "Raw Material", 
            #     {'type': self.type}, 
            #     'Quantity'
            # ) or 0
            self.balance = self.weight
            
            # Calculate the new total by adding the current document's quantity
            # self.total_quantity = total_quantity + self.quantity

	
