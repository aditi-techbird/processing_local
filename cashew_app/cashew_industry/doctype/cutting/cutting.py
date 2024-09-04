# Copyright (c) 2024, techbirdit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Cutting(Document):
   def before_save(self):
    self.rejected_weight = self.boiled_rcn - (self.processed_wholes + self.processed_breaks + self.shell_weight)
    self.balance_wholes = self.processed_wholes
    self.balance_breaks = self.processed_breaks
    if self.boiling_entry and self.boiled_rcn:
        boil = frappe.get_doc("Boiling",self.boiling_entry)
        boil.balance -= self.boiled_rcn
        if boil.balance < 0:
            frappe.throw(f"Input quantity ({self.boiled_rcn} kg) cannot be greater than the available balance quantity ({boil.balance} kg) in Boiling process.")
        boil.save()
        frappe.db.commit()
        frappe.log_error(f"Balance Whole: {boil.balance}, Balance Breaks: {self.boiled_rcn}", "Cutting Before Save")
    
    
    

        
    
        

