from view.notifications_view import NotificationsView
from model.notifications_model import NotificationsModel

class NotificationsController:
    def __init__(self, root_window):
        self.root = root_window
        self.view = NotificationsView(self.root)
        self.model = NotificationsModel()
        self._bind_events()
        
    def _bind_events(self):
        for noti in self.model.get_notifications(self.view.supplier.get()):
            notification_frame, close_button = self.view.create_notification_frame(message=noti[0])
            close_button.configure(command=lambda noti_frame=notification_frame, message=noti[0]: self.remove_noti_frame(noti_frame, message))
        
        self.view.supplier_opt.configure(command=self.refresh_notifications)


    def refresh_notifications(self, opt_value):
        for noti_frame in self.view.scrollable_frame.winfo_children():
            noti_frame.destroy()
        
        for noti in self.model.get_notifications(self.view.supplier.get()):
            notification_frame, close_button = self.view.create_notification_frame(message=noti[0])
            close_button.configure(command=lambda noti_frame=notification_frame, message=noti[0]: self.remove_noti_frame(noti_frame, message))



    def remove_noti_frame(self, notification_frame, message):
        notification_frame.destroy()
        self.model.seen_notification(message)



