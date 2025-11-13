import streamlit as st
import uuid

st.title("Singleton Pattern")

# --- Singleton Class Definition ---
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls)
            cls._instance.id = uuid.uuid4()
            cls._instance.counter = 0
        return cls._instance

    def increment(self):
        self.counter += 1
        return self.counter


# --- Maintain Singleton Across Reruns ---
if "singleton_instance" not in st.session_state:
    st.session_state["singleton_instance"] = Singleton()

singleton = st.session_state["singleton_instance"]
singleton.increment()

# --- Display Results ---
st.subheader("Singleton Instance Information")
st.json({
    "Instance UUID": str(singleton.id),
    "Counter": singleton.counter,
    "Object Memory ID": id(singleton)
})

st.caption(
    "This Singleton instance remains consistent across Streamlit reruns."
)

if st.button("Re-run"):
    st.rerun()
