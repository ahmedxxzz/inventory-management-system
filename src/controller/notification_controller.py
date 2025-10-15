from view.notification_view import NotificationView
from model.notification_model import NotificationModel

class NotificationController:
    def __init__(self, root, db_conn, on_close_callback, distributors):
        self.model = NotificationModel(db_conn)
        self.view = NotificationView(root)
        self.on_close_callback = on_close_callback
        
        # Setup the filter menu
        filter_options = ["الجميع"] + distributors
        self.view.distributor_filter_menu.configure(values=filter_options, command=self._filter_notifications)
        
        self._load_notifications()
        self._bind_events()

    def _load_notifications(self, distributor_filter=None):
        """Fetches notifications based on the filter and populates the Treeview."""
        if distributor_filter == "الجميع":
            distributor_filter = None
            
        notifications = self.model.get_notifications_by_distributor(distributor_filter)
        
        self.view.tree.delete(*self.view.tree.get_children())
            
        for _, date, message, status, _ in notifications:
            status_text = "جديد" if status == 'unseen' else "مقروء"
            tag = status
            self.view.tree.insert("", "end", values=(status_text, message, date), tags=(tag,))

    def _bind_events(self):
        self.view.mark_seen_button.configure(command=self._mark_all_as_seen)

    def _filter_notifications(self, selected_distributor):
        """Callback function for the option menu."""
        self._load_notifications(distributor_filter=selected_distributor)

    def _mark_all_as_seen(self):
        if self.model.mark_all_as_seen():
            # Reload notifications with the current filter
            current_filter = self.view.distributor_filter_menu.get()
            self._load_notifications(distributor_filter=current_filter)
            # Update the main sidebar button
            self.on_close_callback()