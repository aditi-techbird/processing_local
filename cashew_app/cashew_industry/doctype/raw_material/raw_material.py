# Copyright (c) 2024, techbirdit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RawMaterial(Document):
    def before_save(self):
        if self.type == "RCN 48":
            self.rcn_48 = self.quantity
        if self.type == "RCN 49":
            self.rcn_49 = self.quantity
        if self.type == "RCN 50":
            self.rcn_50 = self.quantity
        
            
    #   if self.type and self.quantity and not self.balance:
    #         self.balance = self.quantity