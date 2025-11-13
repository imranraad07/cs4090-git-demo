import streamlit as st

############################################################
# PubSub Core
############################################################

class MessageBroker:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, topic, subscriber):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(subscriber)

    def unsubscribe(self, topic, subscriber):
        if topic in self.subscribers:
            self.subscribers[topic] = [
                s for s in self.subscribers[topic] if s != subscriber
            ]

    def publish(self, topic, data):
        if topic in self.subscribers:
            for s in self.subscribers[topic]:
                s.notify(topic, data)

############################################################
# Subscriber interface
############################################################

class Subscriber:
    def notify(self, topic, data):
        raise NotImplementedError("Must implement notify")


############################################################
# Concrete subscribers
############################################################

class EmailSubscriber(Subscriber):
    def __init__(self):
        self.received = []

    def notify(self, topic, data):
        self.received.append(f"Email received from {topic}: {data}")


class SmsSubscriber(Subscriber):
    def __init__(self):
        self.received = []

    def notify(self, topic, data):
        self.received.append(f"SMS received from {topic}: {data}")


class LogSubscriber(Subscriber):
    def __init__(self):
        self.received = []

    def notify(self, topic, data):
        self.received.append(f"Log entry from {topic}: {data}")


############################################################
# Streamlit PubSub Demo
############################################################

st.title("PubSub Pattern Demo")

broker = MessageBroker()

email_sub = EmailSubscriber()
sms_sub = SmsSubscriber()
log_sub = LogSubscriber()

############################################################
# Subscription controls
############################################################

st.subheader("Enable Subscribers")

use_email = st.checkbox("Email Subscriber")
use_sms = st.checkbox("SMS Subscriber")
use_log = st.checkbox("Log Subscriber")

topic = st.text_input("Topic Name", "orders")
message = st.text_input("Message to Publish", "Order created")

############################################################
# Subscribe dynamically based on UI
############################################################

if use_email:
    broker.subscribe(topic, email_sub)

if use_sms:
    broker.subscribe(topic, sms_sub)

if use_log:
    broker.subscribe(topic, log_sub)


############################################################
# Publish event
############################################################

if st.button("Publish Message"):
    broker.publish(topic, message)
    st.success(f"Message published to topic '{topic}'")

    st.subheader("Subscriber Outputs")

    if use_email:
        st.write("Email Subscriber:")
        for item in email_sub.received:
            st.write(item)

    if use_sms:
        st.write("SMS Subscriber:")
        for item in sms_sub.received:
            st.write(item)

    if use_log:
        st.write("Log Subscriber:")
        for item in log_sub.received:
            st.write(item)
