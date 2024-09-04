import frappe
from frappe import _
from frappe.model.document import Document

class ManualPeeling(Document):
    def on_update(self):
        self.append_sizer_output()
        
    def before_save(self):
        if self.items_pulled ==1 and len(self.manual_peeling_input)>0:
            sizer_doc = frappe.get_doc('Sizer',self.sizer_entry)
            
            # Iterate through the sizer_input items
            for manual_peeling_item in self.manual_peeling_input:
                print("Updated Quantity :", manual_peeling_item.updated_quantity)
                if manual_peeling_item.update_qty==1:
                    if manual_peeling_item.updated_quantity<=0:
                        # Find the corresponding peeled_output item in the Peeling documentsizer_item.item_code
                        for sizer_item in sizer_doc.sizer_output:
                            if sizer_item.item_code == manual_peeling_item.item_code:
                                # Fetch the specific peeled_output item document
                                sizer_out_item = frappe.get_doc("Peeling output", sizer_item.name)
                                
                                # Subtract the sizer input quantity from the peeled output balance quantity
                                if sizer_out_item.balanced_quantity > 0 :
                                    diff = sizer_out_item.balanced_quantity - manual_peeling_item.quantity
                                    manual_peeling_item.updated_quantity = manual_peeling_item.quantity
                                    frappe.db.set_value("Peeling output", sizer_item.name, "balanced_quantity", diff)
                                    manual_peeling_item.update_qty=0
                                break
                    else:
                        frappe.throw(_("You cannot update quantity if updated once before. Kindly create a new Entry for the remaining quantity"))
        if self.manual_peeling_output:
            for entry in self.manual_peeling_output:
                entry.balanced_quantity=float(entry.quantity)
                
    def on_submit(self):
        if self.items_pulled == 1:
            sizer_doc = frappe.get_doc("Sizer", self.sizer_entry)
            for manual_peeling_item in self.manual_peeling_input:
                for sizer_item in sizer_doc.sizer_output:
                    if sizer_item.item_code == manual_peeling_item.item_code and manual_peeling_item.updated_quantity <=0:
                        sizer_out_item = frappe.get_doc("Peeling output", sizer_item.name)
                        if sizer_out_item.balanced_quantity > 0 :
                            diff = sizer_out_item.balanced_quantity - manual_peeling_item.quantity
                            manual_peeling_item.updated_quantity = manual_peeling_item.quantity
                            frappe.db.set_value("Peeling output", sizer_item.name, "balanced_quantity", diff)
                            manual_peeling_item.update_qty=0
                        break
        if self.manual_peeling_output:
            for entry in self.manual_peeling_output:
                entry.balanced_quantity=float(entry.quantity)
        
        
    def append_sizer_output(self):
        try:
            # Fetch the Peeling document
            sizer_doc = frappe.get_doc("Sizer", self.sizer_entry)
            print(f"Fetched Peeling document: {sizer_doc.name}")  # Debugging statement
            # Iterate over the child table rows in Peeling
            
            if self.items_pulled == 0:
                for sizer_item in sizer_doc.sizer_output:
                    # Check if an entry with the same sizer_input already exists
                    if not frappe.db.exists("Cashew Input Items", {"item_code": sizer_item.item_code, "parent": self.name}):
                        self.append('manual_peeling_input', {"doctype":"Cashew Input Items", "item_code": sizer_item.item_code, "item_name":sizer_item.item_name, "quantity":sizer_item.balanced_quantity, "uom":sizer_item.uom})
                # Save the document
                self.items_pulled = 1
                print(f"Updated manual peeling document: {self.name}")  # Debugging statement
            
        except Exception as e:
            # Handle exceptions and log errors
            frappe.log_error(message=frappe.get_traceback(), title=_("Error in append_sizer_output"))
            print(f"Exception occurred: {str(e)}")  # Debugging statement
            frappe.throw(_("An error occurred while appending sizer output."))
            
    
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
            