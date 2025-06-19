from view.Factory_view import FactoryView

class FactoryController:
    def __init__(self, root_window) -> None:
        self.root = root_window
        self.view = FactoryView(self.root)
        