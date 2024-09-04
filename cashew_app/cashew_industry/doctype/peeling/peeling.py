# Copyright (c) 2024, techbirdit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


# class Peeling(Document):
#     def before_save(self):
#         if self.cutting_entry and self.quantity:
#             cutting = frappe.get_doc("Cutting",self.cutting_entry)
#             if self.type_of_input == "NW Wholes":
#                 self.quantity = cutting.balance_wholes
#                 print("quantity is : "+str(self.quantity))
#                 diff = cutting.balance_wholes-self.quantity
#                 frappe.db.set_value("Cutting",self.cutting_entry,"balance_wholes",diff)
#             else:
#                 self.quantity = cutting.balance_breaks
#                 print("quantity is : "+str(self.quantity))
#                 diff = cutting.balance_breaks-self.quantity
#                 frappe.db.set_value("Cutting",self.cutting_entry,"balance_breaks",diff)
#         if self.peeled_output_items:
#             for entry in self.peeled_output_items:
#                 entry.balanced_quantity=float(entry.quantity)
# class Peeling(Document):
#     def before_save(self):
#         if self.cutting_entry and self.quantity:
#             cutting = frappe.get_doc("Cutting", self.cutting_entry)
#             if self.type_of_input == "NW Wholes":
#                 # Assign the cutting balance to the quantity field
#                 self.quantity = cutting.balance_wholes
#                 print("quantity is:", self.quantity)  # This should display the correct value
#                 diff = cutting.balance_wholes - self.quantity
#                 frappe.db.set_value("Cutting", self.cutting_entry, "balance_wholes", diff)
#             else:
#                 # Assign the cutting balance to the quantity field
#                 self.quantity = cutting.balance_breaks
#                 print("quantity is:", self.quantity)  # This should display the correct value
#                 diff = cutting.balance_breaks - self.quantity
#                 frappe.db.set_value("Cutting", self.cutting_entry, "balance_breaks", diff)
            
#         if self.peeled_output_items:
#             for entry in self.peeled_output_items:
#                 entry.balanced_quantity = float(entry.quantity)

class Peeling(Document):
    def before_save(self):
        if self.cutting_entry and self.quantity:
            cutting = frappe.get_doc("Cutting", self.cutting_entry)
            if self.type_of_input == "NW Wholes":
                # Use current balance_wholes to set quantity
                # self.quantity = cutting.balance_wholes
                # print(f"quantity is: {self.quantity}")
                # Update the balance properly by subtracting quantity
                diff = cutting.balance_wholes - self.quantity
                print("cutting.balance_wholes: ",cutting.balance_wholes)
                if diff < 0:
                    frappe.throw("Quantity exceeds available balance in Wholes.")
                frappe.db.set_value("Cutting", self.cutting_entry, "balance_wholes", diff)
                # cutting.balance_wholes = diff
            else:
                # Use current balance_breaks to set quantity
                # self.quantity = cutting.balance_breaks
                # print(f"quantity is: {self.quantity}")
                # Update the balance properly by subtracting quantity
                diff = cutting.balance_breaks - self.quantity
                if diff < 0:
                    frappe.throw("Quantity exceeds available balance in Breaks.")
                frappe.db.set_value("Cutting", self.cutting_entry, "balance_breaks", diff)
                print("cutting.balance_breaks: ",str(cutting.balance_breaks))
            
            # Save the Cutting document after making changes
            # cutting.save()

        if self.peeled_output_items:
            for entry in self.peeled_output_items:
                entry.balanced_quantity = float(entry.quantity)

  
                
                
  