from view.dashboard_view import DashboardView
from model.dashboard_model import DashboardModel

class DashboardController:
    def __init__(self, root_window):
        self.view = DashboardView(root_window)