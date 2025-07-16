from view.dashboard_view import DashboardView
from model.dashboard_model import DashboardModel

class DashboardController:
    def __init__(self, root_window):
        self.view = DashboardView(root_window)
        self.model = DashboardModel()
        
        self.view.populate_treeview(self.view.tree1,self.model.get_product_sales_by_period(self.view.opt1_value.get(), self.view.supplier.get()))
        self.view.populate_treeview(self.view.tree2,self.model.get_profit(self.view.opt2_value.get(), self.view.supplier.get()))

        self._bind_events()
        
        
    def _bind_events(self):
        self.view.opt1.configure(command=self.most_sold_date_change)
        self.view.opt2.configure(command=self.profit_date_change)
        self.view.supplier_opt.configure(command=self.supplier_change)


    def supplier_change(self, new_value):
        self.view.populate_treeview(self.view.tree1,self.model.get_product_sales_by_period(self.view.opt1_value.get(), self.view.supplier.get()))
        self.view.populate_treeview(self.view.tree2,self.model.get_profit(self.view.opt2_value.get(), self.view.supplier.get()))


    def most_sold_date_change(self, new_value):
        self.view.populate_treeview(self.view.tree1,self.model.get_product_sales_by_period(self.view.opt1_value.get(), self.view.supplier.get()))


    def profit_date_change(self, new_value):
        self.view.populate_treeview(self.view.tree2,self.model.get_profit(self.view.opt2_value.get(), self.view.supplier.get()))



        
        