from view.Customer_compnents_view.customer_account_details_view import CustomerAccountDetailsView
from model.Customer_compnents_model.customer_account_details_model import CustomerAccountDetailsModel
from controller.Customer_compnents_controller.show_details_popup_controller import ShowDetailsPopupController
class CustomerAccountDetailsController:
    def __init__(self, root, frames, customer_name, supplier ):
        self.root = root
        self.frames = frames
        self.supplier = supplier
        self.customer_name = customer_name
        self.view = CustomerAccountDetailsView(self.root, self.customer_name)
        self.model = CustomerAccountDetailsModel(self.customer_name, self.supplier)
        
        
        self.fill_data()
        self.view.populate_treeview(self.model.get_customer_account_details())
        
        self._bind_events()
                
    
    
    def _bind_events(self):
        self.view.back_btn.configure(command=self.back)
        self.view.report_btn.configure(command=self.report)
        self.view.tree.bind("<Double-1>", self.tree_double_click)
    
    
    
    def fill_data(self ):
        cus_money, cus_quantity = self.model.get_customer_data()
        self.view.money_lbl.configure(text=f'الرصيد الحالي : \n{cus_money}')
        self.view.quantity_lbl.configure(text=f'الكمية الحالية : \n{cus_quantity}')
    
    
    
    def back(self):
        for frame in self.frames:
            frame.destroy()
        from controller.Customer_compnents_controller.customer_account_controller import CustomerAccountController
        
        customers_accounts = CustomerAccountController(self.root, self.supplier, self.frames)
        self.frames.append(customers_accounts.view)


    def report(self):
        from controller.Customer_compnents_controller.report_controller import ReportController
        ReportController(self.model.get_cus_id_by_name(self.customer_name), self.supplier)


    def tree_double_click(self, event):
        """
        Handles the double-click event on the Treeview.
        Retrieves the id and operation_type of the double-clicked row
        and calls the duple_click function.
        """
        # Get the item (row) that was double-clicked
        item_id = self.view.tree.identify_row(event.y)
        
        if item_id:
            # Get the values of the clicked item
            values = self.view.tree.item(item_id, 'values')
            
            # Ensure values are not empty and have enough elements
            if values and len(values) >= len(self.view.tree_columns):
                # Get the index of 'id' and 'operation_type' from self.tree_columns
                try:
                    id_index = self.view.tree_columns.index('id')
                    operation_type_index = self.view.tree_columns.index('operation_type')

                    # Extract the id and operation_type
                    row_id = values[id_index]
                    operation_type = values[operation_type_index]
                    
                    # Call the duple_click function with the extracted values
                    self.show_details(row_id, operation_type)
                except ValueError as e:
                    print(f"Error: Column not found in tree_columns: {e}")
            else:
                print("Clicked row has incomplete data.")
        else:
            print("No row identified at double-click position.")


    def show_details(self, row_id, operation_type):
        popup = ShowDetailsPopupController(self.root, row_id, operation_type)