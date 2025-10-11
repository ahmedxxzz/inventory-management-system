from view.Inventory.inventory_dashboard_view import InventoryDashboardView
from model.Inventory.inventory_dashboard_model import InventoryDashboardModel

class InventoryDashboardController:
    def __init__(self, frame, db_conn):
        self.frame = frame
        self.db_conn = db_conn
        self.view = InventoryDashboardView(self.frame)
        self.model  = InventoryDashboardModel(self.db_conn)
        
        self._bind_events()
        self.view.populate_treeview(self.view.tree1,self.model.get_product_sales_by_period(self.view.opt1_value.get(), self.view.distributor.get()))
        self.view.populate_treeview(self.view.tree2,self.model.get_profit(self.view.opt2_value.get(), self.view.distributor.get()))


    def _bind_events(self):
        self.view.opt1.configure(command=self.most_sold_date_change)
        self.view.opt2.configure(command=self.profit_date_change)
        self.view.distributor_opt.configure(values = ['الجميع'] + self.model.get_distributors(), command=self.distributor_change, )


    def distributor_change(self, new_value):
        self.view.populate_treeview(self.view.tree1,self.model.get_product_sales_by_period(self.view.opt1_value.get(), self.view.distributor.get()))
        self.view.populate_treeview(self.view.tree2,self.model.get_profit(self.view.opt2_value.get(), self.view.distributor.get()))


    def most_sold_date_change(self, new_value):
        self.view.populate_treeview(self.view.tree1,self.model.get_product_sales_by_period(self.view.opt1_value.get(), self.view.distributor.get()))


    def profit_date_change(self, new_value):
        self.view.populate_treeview(self.view.tree2,self.model.get_profit(self.view.opt2_value.get(), self.view.distributor.get()))



        
        