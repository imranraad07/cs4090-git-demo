import streamlit as st

############################################################
# Observer interface
############################################################

class Observer:
    def update(self, message):
        raise NotImplementedError("Must implement update")

############################################################
# Concrete observers
############################################################

class EmailNotifier(Observer):
    def __init__(self):
        self.messages = []

    def update(self, message):
        self.messages.append(f"Email sent: {message}")

class SMSNotifier(Observer):
    def __init__(self):
        self.messages = []

    def update(self, message):
        self.messages.append(f"SMS sent: {message}")

class ActivityLogObserver(Observer):
    def __init__(self):
        self.messages = []

    def update(self, message):
        self.messages.append(f"Log entry: {message}")

############################################################
# Subject (observable)
############################################################

class OrderStatus:
    def __init__(self):
        self.observers = []
        self.status = "Pending"

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers = [o for o in self.observers if o != observer]

    def set_status(self, new_status):
        self.status = new_status
        self.notify_observers(f"Order status changed to {new_status}")

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

############################################################
# Streamlit UI
############################################################

st.title("Observer Pattern Demo")

status_options = ["Pending", "Processing", "Shipped", "Delivered"]

status_manager = OrderStatus()

email_obs = EmailNotifier()
sms_obs = SMSNotifier()
log_obs = ActivityLogObserver()

use_email = st.checkbox("Enable Email Observer")
use_sms = st.checkbox("Enable SMS Observer")
use_log = st.checkbox("Enable Log Observer")

if use_email:
    status_manager.attach(email_obs)

if use_sms:
    status_manager.attach(sms_obs)

if use_log:
    status_manager.attach(log_obs)

chosen = st.selectbox("Choose new order status", status_options)

if st.button("Update Status"):
    status_manager.set_status(chosen)
    st.success(f"Status updated to {chosen}")

    st.subheader("Observer Outputs")

    if use_email:
        st.write("Email Observer:")
        for m in email_obs.messages:
            st.write(m)

    if use_sms:
        st.write("SMS Observer:")
        for m in sms_obs.messages:
            st.write(m)

    if use_log:
        st.write("Activity Log:")
        for m in log_obs.messages:
            st.write(m)
