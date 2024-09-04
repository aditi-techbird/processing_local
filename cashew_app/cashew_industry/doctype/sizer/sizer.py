# Copyright (c) 2024, techbirdit and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

class Sizer(Document):
    def on_update(self):
        self.append_pilling_output()
        
    def before_save(self):
        if self.items_pulled == 1 and len(self.sizer_input)>0:
            # self.update_pilled_output_quantities()
            peeling_doc = frappe.get_doc("Peeling", self.peeling_entry)

            # Iterate through the sizer_input items
            for sizer_item in self.sizer_input:
                print("Updated Quantity :", sizer_item.updated_quantity)
                if sizer_item.update_qty==1:
                    if sizer_item.updated_quantity<=0:
                        # Find the corresponding peeled_output item in the Peeling documentsizer_item.item_code
                        for peeling_item in peeling_doc.peeled_output_items:
                            if peeling_item.item_code == sizer_item.item_code:
                                # Fetch the specific peeled_output item document
                                peeled_out_item = frappe.get_doc("Peeling output", peeling_item.name)
                                
                                # Subtract the sizer input quantity from the peeled output balance quantity
                                if peeled_out_item.balanced_quantity > 0 :
                                    diff = peeled_out_item.balanced_quantity - sizer_item.quantity
                                    sizer_item.updated_quantity = sizer_item.quantity
                                    frappe.db.set_value("Peeling output", peeling_item.name, "balanced_quantity", diff)
                                    sizer_item.update_qty=0
                                break
                    else:
                        frappe.throw(_("You cannot update quantity if updated once before. Kindly create a new Entry for the remaining quantity"))
        if self.sizer_output:
            for entry in self.sizer_output:
                entry.balanced_quantity=float(entry.quantity)
                
    def on_submit(self):
        if self.items_pulled == 1:
            peeling_doc = frappe.get_doc("Peeling", self.peeling_entry)
            for sizer_item in self.sizer_input:
                for peeling_item in peeling_doc.peeled_output_items:
                    if peeling_item.item_code == sizer_item.item_code and sizer_item.updated_quantity <=0:
                        peeled_out_item = frappe.get_doc("Peeling output", peeling_item.name)
                        if peeled_out_item.balanced_quantity > 0 :
                            diff = peeled_out_item.balanced_quantity - sizer_item.quantity
                            sizer_item.updated_quantity = sizer_item.quantity
                            frappe.db.set_value("Peeling output", peeling_item.name, "balanced_quantity", diff)
                            sizer_item.update_qty=0
                        break
        if self.sizer_output:
            for entry in self.sizer_output:
                entry.balanced_quantity=float(entry.quantity)
        
        
    def append_pilling_output(self):
        try:
            # Fetch the Peeling document
            peeling_doc = frappe.get_doc("Peeling", self.peeling_entry)
            print(f"Fetched Peeling document: {peeling_doc.name}")  # Debugging statement
            # Iterate over the child table rows in Peeling
            
            if self.items_pulled == 0:
                for peeling_item in peeling_doc.peeled_output_items:
                    # Check if an entry with the same sizer_input already exists
                    if not frappe.db.exists("Cashew Input Items", {"item_code": peeling_item.item_code, "parent": self.name}):
                        self.append('sizer_input', {"doctype":"Cashew Input Items", "item_code": peeling_item.item_code, "item_name":peeling_item.item_name, "quantity":peeling_item.balanced_quantity, "uom":peeling_item.uom})
                # Save the document
                self.items_pulled = 1
                print(f"Updated Sizer document: {self.name}")  # Debugging statement
            
        except Exception as e:
            # Handle exceptions and log errors
            frappe.log_error(message=str(e), title=_("Error in append_pilling_output"))
            print(f"Exception occurred: {str(e)}")  # Debugging statement
            frappe.throw(_("An error occurred while appending peeling output."))
            
    
    # def update_pilled_output_quantities(self):
    #     try:
    #         # Fetch the Peeling document
    #         peeling_doc = frappe.get_doc("Peeling", self.peeling_entry)

    #         # Iterate through the sizer_input items
    #         for sizer_item in self.sizer_input:
    #             # Find the corresponding peeled_output item in the Peeling documentsizer_item.item_code
    #             for peeling_item in peeling_doc.peeled_output_items:
    #                 if peeling_item.item_code == sizer_item.item_code and sizer_item.update_qty==1 and sizer_item.updated_quantity <=0:
    #                     # Fetch the specific peeled_output item document
    #                     peeled_out_item = frappe.get_doc("Peeling output", peeling_item.name)
                        
    #                     # Subtract the sizer input quantity from the peeled output balance quantity
    #                     if peeled_out_item.balanced_quantity > 0 :
    #                         diff = peeled_out_item.balanced_quantity - sizer_item.quantity
    #                         sizer_item.updated_quantity = sizer_item.quantity
    #                         frappe.db.set_value("Peeling output", peeling_item.name, "balanced_quantity", diff)
    #                         sizer_item.update_qty=0
                            
    #                     break
            

    #     except Exception as e:
    #         # Handle exceptions and log errors
    #         frappe.log_error(message= frappe.get_traceback(), title=_("Error in update_pilled_output_quantities"))
    #         frappe.throw(_("An error occurred while updating peeled output quantities."))