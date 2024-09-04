import frappe
from frappe import _
from frappe.model.document import Document

class Grading(Document):
    def on_update(self):
        self.append_manual_peeling_output()
        
    def before_save(self):
        if self.items_pulled == 1 and len(self.grading_input)>0:
            manual_peeling_doc = frappe.get_doc("Manual Peeling",self.manual_peeling_entry)
            for grading_item in self.grading_input:
                print("updated Quantity :",grading_item.updated_quantity)
                if grading_item.update_qty == 1:
                    if grading_item.updated_quantity<=0:
                        for manual_peeling_item in manual_peeling_doc.manual_peeling_output:
                            if manual_peeling_item.item_code == grading_item.item_code:
                                manual_peeling_out_doc = frappe.get_doc("Manual Peeling Output",manual_peeling_item.name)
                                if manual_peeling_out_doc.balanced_quantity >0 :
                                    diff = manual_peeling_out_doc.balanced_quantity - grading_item.quantity
                                    grading_item.updated_quantity = grading_item.quantity
                                    frappe.db.set_value("Peeling output",manual_peeling_doc.name,"balanced_quantity",diff)
                                    grading_item.update_qty = 0
                                break
                    else:
                        frappe.throw(_("you cannot update quantity if updated once before.kindly create a new entry for the remaining quantity."))
        if self.grading_output:
            for entry in self.grading_output:
                entry.balanced_quantity = float(entry.quantity)
                
    def on_submit(self):
        if self.items_pulled ==1:
            manual_peeling_doc = frappe.get_doc("Manual Peeling",self.manual_peeling_entry)
            for grading_item in self.grading_input:
                for manual_pilling_item in manual_peeling_doc.manual_peeling_output:
                    if manual_pilling_item.item_code == grading_item.item_code and grading_item.updated_quantity <=0:
                        manual_pilling_out_item = frappe.get_doc("Peeling output", manual_pilling_item.name)
                        if manual_pilling_out_item.balanced_quantity > 0 :
                            diff = manual_pilling_out_item.balanced_quantity - grading_item.quantity
                            grading_item.updated_quantity = grading_item.quantity
                            frappe.db.set_value("Peeling output", manual_pilling_item.name, "balanced_quantity", diff)
                            grading_item.update_qty=0
                        break
        if self.grading_output:
            for entry in self.grading_output:
                entry.balanced_quantity=float(entry.quantity)
        if self.grading_output:
             self.create_stock_entries()
        
        
    def append_manual_peeling_output(self):
        try:
            # Fetch the Peeling document
            manual_pilling_doc = frappe.get_doc("Manual Peeling", self.manual_peeling_entry)
            print(f"Fetched Peeling document: {manual_pilling_doc.name}")  # Debugging statement
            # Iterate over the child table rows in Peeling
            
            if self.items_pulled == 0:
                for manual_pilling_item in manual_pilling_doc.manual_peeling_output:
                    # Check if an entry with the same sizer_input already exists
                    if not frappe.db.exists("Cashew Input Items", {"item_code":manual_pilling_item.item_code, "parent": self.name}):
                        self.append('grading_input', 
                                  {"doctype":"Cashew Input Items", 
                                   "item_code": manual_pilling_item.item_code, "item_name":manual_pilling_item.item_name,
                                   "quantity":manual_pilling_item.balanced_quantity, 
                                   "uom":manual_pilling_item.uom})
                # Save the document
                self.items_pulled = 1
                print(f"Updated grading document: {self.name}")  # Debugging statement
            
        except Exception as e:
            # Handle exceptions and log errors
            frappe.log_error(message=frappe.get_traceback(), title=_("Error in append_manual peeling_output"))
            print(f"Exception occurred: {str(e)}")  # Debugging statement
            frappe.throw(_("An error occurred while appending manual Peeling output."))
    
    def create_stock_entries(self):
        stock_entry_item = []
        for output_item in self.grading_output:
            item_dict ={
                "item_code": output_item.item_code,
                "item_name": output_item.item_name,
                "qty": output_item.balanced_quantity,
                "uom": output_item.uom,
                "t_warehouse": self.target_warehouse # Target warehouse
                }
            stock_entry_item.append(item_dict)
        
        stock_entry = frappe.get_doc(
            {
                "doctype":"Stock Entry",
                "stock_entry_type" : "Material Receipt" , # or "Material Issue" depending on your need
                "posting_date" :frappe.utils.nowdate(),
                "posting_time" : frappe.utils.nowtime(),
                "purpose" :"Material Receipt" ,
                "items":  stock_entry_item
            }
        ).insert(ignore_permissions=True)
        stock_entry.submit()
        
    
    
    
    
                        
                    
            
                                    
                                    
            
    # # =========================================================================================
    # def before_save(self):
    #     self.append_manual_peeling_output()
    #     if self.items_pulled == 1:
    #         self.update_manual_peeling_output_quantities()
    #     if self.grading_output:
    #         for entry in self.grading_output:
    #             # Check if balanced_quantity is None and handle it
    #             # if entry.balanced_quantity is None:
    #             #     frappe.throw(_("Balanced quantity cannot be None. Please provide a valid quantity."))

    #             # Ensure balanced_quantity is a valid float before proceeding
    #             # try:
    #                 # balanced_quantity = float(entry.balanced_quantity)
    #             # except ValueError:
    #             #     frappe.throw(_("Balanced quantity must be a number."))
                    
    #             # if balanced_quantity <= 0:  # Prevent direct zeroing without reason
    #             #     frappe.throw(_("Balanced quantity cannot be zero or negative without valid operations."))

    #             # Safely convert entry.quantity to float and assign to balanced_quantity
    #             entry.balanced_quantity = float(entry.quantity)

    # # def on_update(self):
    # #     self.update_pilled_output_quantities()
    # def on_submit(self):
    #     if self.grading_output:
    #         self.create_stock_entries()
        
    
    # def append_manual_peeling_output(self):
    #     try:
    #         # Fetch the Sizer document
    #         manual_peeling_doc = frappe.get_doc("Manual Peeling", self.manual_peeling_entry)
    #         print(f"Fetched manual peeling document: {manual_peeling_doc.name}")  # Debugging statement
            
    #         if self.items_pulled == 0:
    #             for manual_peeling_item in manual_peeling_doc.manual_peeling_output:
    #                 # Debugging statement for each item
    #                 print(f"Processing item: {manual_peeling_item.item_code} with quantity {manual_peeling_item.balanced_quantity}")

    #                 # Check if an entry with the same item_code already exists in manual_peeling_input
    #                 if not frappe.db.exists("Cashew Input Items", {"item_code": manual_peeling_item.item_code, "parent": self.name}):
    #                     self.append('grading_input', {
    #                         "doctype": "Cashew Input Items", 
    #                         "item_code": manual_peeling_item.item_code, 
    #                         "item_name": manual_peeling_item.item_name, 
    #                         "quantity": manual_peeling_item.balanced_quantity, 
    #                         "uom": manual_peeling_item.uom
    #                     })
    #                     print(f"Appended item: {manual_peeling_item.item_code} to grading_input")  # Debugging statement

    #             # Mark items as pulled
    #             self.items_pulled = 1
    #             print(f"Items pulled and updated in grading_input for document: {self.name}")  # Debugging statement
            
    #     except Exception as e:
    #         # Handle exceptions and log errors
    #         frappe.log_error(message=frappe.get_traceback(), title=_("Error in append_manual_peeling_output"))
    #         print(f"Exception occurred: {str(e)}")  # Debugging statement
    #         frappe.throw(_("An error occurred while appending manual peeling output."))
    
    # def update_manual_peeling_output_quantities(self):
    #     try:
    #         manual_peeling_doc = frappe.get_doc("Manual Peeling", self.manual_peeling_entry)

    #         for grading_item in self.grading_input:
    #             if grading_item.update_qty == 1:
    #                 for manual_peeling_item in manual_peeling_doc.manual_peeling_output:
    #                     if manual_peeling_item.item_code == grading_item.item_code:
    #                         manual_peeling_output_item = frappe.get_doc("Peeling output", manual_peeling_item.name)

    #                         # Ensure we'rmanual_peeling_output_iteme not incorrectly zeroing out quantities
    #                         if manual_peeling_output_item.balanced_quantity > 0:
    #                             diff = manual_peeling_output_item.balanced_quantity - grading_item.quantity
    #                             if diff < 0:  # Check if the diff would result in a negative quantity
    #                                 frappe.throw(_("Resulting quantity cannot be negative for item: {0}").format(manual_peeling_output_item.item_code))
                                
    #                             # Update balanced_quantity
    #                             frappe.db.set_value("Peeling output", manual_peeling_output_item.name, "balanced_quantity", diff)
    #                             grading_item.update_qty = 0
    #                             print(f"Updated balanced quantity for item: {manual_peeling_output_item.item_code}")  # Debugging statement
    #                         break

    #     except Exception as e:
    #         frappe.log_error(message=frappe.get_traceback(), title=_("Error in update_manual_peeling_output_quantities"))
    #         frappe.throw(_("An error occurred while updating manual peeling  output quantities."))
    
    # def create_stock_entries(self):
    #     stock_entry_item = []
    #     for output_item in self.grading_output:
    #         item_dict ={
    #             "item_code": output_item.item_code,
    #             "item_name": output_item.item_name,
    #             "qty": output_item.balanced_quantity,
    #             "uom": output_item.uom,
    #             "t_warehouse": self.target_warehouse # Target warehouse
    #             }
    #         stock_entry_item.append(item_dict)
        
    #     stock_entry = frappe.get_doc(
    #         {
    #             "doctype":"Stock Entry",
    #             "stock_entry_type" : "Material Receipt" , # or "Material Issue" depending on your need
    #             "posting_date" :frappe.utils.nowdate(),
    #             "posting_time" : frappe.utils.nowtime(),
    #             "purpose" :"Material Receipt" ,
    #             "items":  stock_entry_item
    #         }
    #     ).insert(ignore_permissions=True)
    #     stock_entry.submit()
        
            
        
